# import os
import time
import logging

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

from elastic_app.constants import ES_HOST, ES_PORT, ES_INDEX, ES_QUERY_NESTED_UNIFIED

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


def search(text="coronavirus", bodyfun=ES_QUERY_NESTED_UNIFIED, index=ES_INDEX, host=ES_HOST, port=ES_PORT):
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


def find_answers(statement, index=ES_INDEX, host=ES_HOST, port=ES_PORT):
    """ Query Elasticsearch using statement as query string and format results as list of 8-tuples """
    global QABOT
    t0 = time.time()
    query_results = search(text=statement, index=index, host=host, port=port)
    results = []
    for i, doc in enumerate(query_results.get('hits', query_results).get('hits', query_results)):
        if i < 5 and time.time() - t0 < 10.:
            for j, highlight in enumerate(doc.get('inner_hits', doc).get('text', doc).get('hits', doc).get('hits', {})):
                snippet = ' '.join(highlight.get('highlight', {}).get('text.section_content', []))
                bot_reply = ''
                if j < 3 and time.time() - t0 < 10.:
                    try:
                        log.warning(f'qary.__version__: {qary.__version__}')
                        log.warning(f'QABOT: {QABOT}')
                        log.warning(f'QABOT.__class__: {QABOT.__class__}')
                        log.warning(f'Bot.__bases__: {QABOT.__class__.__bases__}')
                        log.warning(f'QABOT.context: {QABOT.context}')
                        QABOT.reset_context(context={'doc': {'text': snippet}})
                        log.warning(f'QABOT.context after reset: {QABOT.context}')
                        bot_reply = QABOT.reply(statement)
                    except Exception as e:
                        log.warning(f'reset_context or .reply failed: {e}')
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
