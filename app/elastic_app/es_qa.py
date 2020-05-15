# import os
import time
import logging

from elastic_app.constants import ES_HOST, ES_PORT, ES_INDEX
from elastic_app.es_search import find_snippets, sorted_dicts

import qary  # noqa
from qary.skills.qa_bots import Bot

BOT_PERSONALITIES = ['qa']  # 'glossary,faq'.split(',')

QABOT = Bot()

log = logging.getLogger(__name__)

CLIENT = None


def find_answers(statement, index=ES_INDEX, host=ES_HOST, port=ES_PORT, timeout=100, max_docs=20, max_sections=10):
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
            QABOT.reset_context(
                context={'doc': {'text': modified_snippet}})
            log.warning(f'QABOT.context after reset: {QABOT.context}')
            bot_reply = QABOT.reply(statement, context=modified_snippet)
        except Exception as e:
            log.error(f'reset_context or .reply failed: {e}')
            bot_reply = ''
            break
        hit['reply'] = bot_reply
        results.append(hit)

    results = sorted_dicts(results, key='reply', keyfun=len, reverse=True)
    return results
