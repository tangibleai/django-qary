import time
import logging

from elastic_app.constants import ES_HOST, ES_PORT, ES_INDEX
from elastic_app.es_search import find_snippets

import qary  # noqa
from qary.skills.qa_bots import Bot

BOT_PERSONALITIES = ['qa']  # 'glossary,faq'.split(',')

QABOT = Bot()

log = logging.getLogger(__name__)

CLIENT = None


def sorted_dicts(iterable_of_dicts, key=None, reverse=True):
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
    return sorted(tuple_of_dicts, key=lambda x: x[key], reverse=reverse)


def find_answers(statement, index=ES_INDEX, host=ES_HOST, port=ES_PORT, timeout=100, max_docs=50, max_sections=10):
    """ Query Elasticsearch using statement as query string and format results as list of 8-tuples """
    global QABOT
    t0 = time.time()
    query_results = find_snippets(statement=statement, index=index, host=host, port=port)
    results = []
    for i, doc in enumerate(query_results):
        hit = doc
        snippet = doc.get('snippet', doc)
        modified_snippet = snippet.replace('<em>', '').replace('</em>', '')
        if i > max_docs or time.time() - t0 > timeout:
            break
        try:
            log.warning(f'QABOT.context after reset: {QABOT.context}')
            bot_reply = QABOT.reply(statement, context=modified_snippet)
            hit['reply'] = bot_reply[0][1]
            hit['reply_score'] = bot_reply[0][0]
        except Exception as e:
            hit['reply'] = ''
            hit['reply_score'] = float(0)
            log.error(f'reset_context or .reply failed: {e}')
            pass
        results.append(hit)

    results = sorted_dicts(results, key='reply_score', keyfun=len, reverse=True)
    return results
