# import os
import time
import logging

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

from elastic_app.constants import ES_HOST, ES_PORT, ES_INDEX, ES_QUERY_FLAT

import qary  # noqa
from qary.skills.qa_bots import Bot

# BOT_PERSONALITIES = ['qa']  # 'glossary,faq'.split(',')

QABOT = Bot()


log = logging.getLogger(__name__)

CLIENT = None


def connect_and_ping(host=ES_HOST, port=ES_PORT, elastic_timeout=None, retry_timeout=2, sleep_time=.4):
    t0 = time.time()
    global CLIENT
    log.info("Connecting to ElasticSearch server at {host}:{port} using {CLIENT}...")
    if not CLIENT:
        log.info(f"Connecting to ElasticSearch server at {host}:{port}")
        CLIENT = Elasticsearch(f'{host}:{port}')
    if CLIENT and not CLIENT.ping() and retry_timeout > 0:
        log.error(f"Unable to find ElasticSearch server at {host}:{port}\n    Trying for {retry_timeout}s more.")
        time.sleep(sleep_time)
        retry_timeout -= time.time() - t0
        CLIENT = connect_and_ping(host=host, port=port,
                                  elastic_timeout=elastic_timeout, retry_timeout=retry_timeout,
                                  sleep_time=min(max(sleep_time * 1.7, .1), 28))
    return CLIENT


def search(text="coronavirus", bodyfun=ES_QUERY_FLAT, index=ES_INDEX, host=ES_HOST, port=ES_PORT):
    """ Full text search within an ElasticSearch index (''=all indexes) for the indicated text """
    global CLIENT
    log.warn(f"Attempting to connect to '{host}:{port}'...")
    client = (CLIENT or
              connect_and_ping(host=host, port=port, elastic_timeout=None, retry_timeout=2) or
              Elasticsearch(f'{host}:{port}'))
    log.warn(f"Attempting to search for text='{text}'\n in index='{index}' using client={client}\n")
    try:
        return client.search(body=bodyfun(query=text), index=index)
    except NotFoundError as e:
        log.error(f"{e}:\n    Unable to find any records on {host}:{port}, "
                  f"perhaps because there is no index named '{index}'")
        return {}


def search_hits(text, index=ES_INDEX, host=ES_HOST, port=ES_PORT):
    """ Returns inner hits list of objects from Elasticsearch results for query `text` """
    raw_results = search(text=text, index=index, host=host, port=port)
    return raw_results.get('hits', {}).get('hits', [])


def find_snippets(statement, index=ES_INDEX, host=ES_HOST, port=ES_PORT):
    """ Query Elasticsearch using statement as query string and format results as list of 8-tuples """
    query_results = search(text=statement, index=index, host=host, port=port)
    results = []
    for i, doc in enumerate(query_results.get('hits', query_results).get('hits', query_results)):
        # log.debug('str(doc)')
        # results.append(('_title', 'doc._score', '_source', 'snippet', 'section_num', 'section_title', 'snippet._score', doc))
        for highlight in doc.get('inner_hits', doc).get('text', doc).get('hits', doc).get('hits', {}):
            snippet = ' '.join(highlight.get('highlight', {}).get('text.section_content', []))
            bot_reply = ''
            hit = dict(
                title=doc['_source']['title'],
                score=doc['_score'],
                source=doc['_source']['source'],
                snippet=snippet,
                section_num=highlight['_source']['section_num'],
                section_title=highlight['_source']['section_title'],
                section_score=highlight['_score'],
                reply=bot_reply)
            results.append(hit)

    return results


def sorted_dicts(iterable_of_dicts, key=None, reverse=False, keyfun=None):
    """ Like sorted(), only `key` is the Mapping key used to look up the sort key

    >>> results = [dict(zip('abc', 'a ab abc'.split()))]
    >>> results.append(dict(zip('ab', 'yz wxyz'.split())))
    >>> sorted_dicts(results, key='a')
    [{'a': 'a', 'b': 'ab', 'c': 'abc'}, {'a': 'yz', 'b': 'wxyz'}]
    >>> sorted_dicts(results, key='a', reverse=True)
    [{'a': 'yz', 'b': 'wxyz'}, {'a': 'a', 'b': 'ab', 'c': 'abc'}]
    >>> sorted_dicts(results, key='c', reverse=True, keyfun=len)
    [{'a': 'a', 'b': 'ab', 'c': 'abc'}, {'a': 'yz', 'b': 'wxyz'}]
    >>> sorted_dicts(results, key='a', reverse=True)
    [{'a': 'yz', 'b': 'wxyz'}, {'a': 'a', 'b': 'ab', 'c': 'abc'}]
    """
    tuple_of_dicts = tuple(iterable_of_dicts)
    if key is None:
        iterable_of_dicts = tuple(iterable_of_dicts)
        key = tuple(tuple_of_dicts[0].keys())[0]
        log.warning('No key specified, so first key in first dictionary ({key}) was used as sort key.')
    firstvalue = tuple_of_dicts[0][key]
    valuetype = type(firstvalue)
    keyfun = valuetype if keyfun is None else keyfun
    nullvalue = float('nan') if isinstance(firstvalue, (float, int)) else ''
    return sorted(tuple_of_dicts, key=lambda x: keyfun(x.get(key, nullvalue)), reverse=reverse)


def find_answers(statement, index=ES_INDEX, host=ES_HOST, port=ES_PORT, timeout=100, max_docs=20, max_sections=10):
    """ Query Elasticsearch using statement as query string and format results as list of 8-tuples """
    global QABOT
    t0 = time.time()
    query_results = search(text=statement, index=index, host=host, port=port)
    results = []
    for i, doc in enumerate(query_results.get('hits', query_results).get('hits', query_results)):
        if i > max_docs or time.time() - t0 > timeout:
            break
        for j, highlight in enumerate(doc.get('inner_hits', doc).get('text', doc).get('hits', doc).get('hits', {})):
            snippet = ' '.join(highlight.get('highlight', {}).get('text.section_content', []))
            tags = doc.get('tags', doc)
            snippet_modified = '\n'.join(tags, snippet)
            bot_reply = ''
            if j > max_sections or time.time() - t0 > timeout:
                break
            try:
                QABOT.reset_context(
                    context={'doc': {'text':
                                     snippet.replace('<em>', '').replace('</em>', '')}})
                log.warning(f'QABOT.context after reset: {QABOT.context}')
                bot_reply = QABOT.reply(statement)
            except Exception as e:
                log.error(f'reset_context or .reply failed: {e}')
                bot_reply = ''
                break
            hit = dict(
                title=doc['_source']['title'],
                score=doc['_score'],
                source=doc['_source']['source'],
                snippet=snippet_modified,
                section_num=highlight['_source']['section_num'],
                section_title=highlight['_source']['section_title'],
                section_score=highlight['_score'],
                reply=bot_reply)
            results.append(hit)

    results = sorted_dicts(results, key='reply', keyfun=len, reverse=True)
    return results
