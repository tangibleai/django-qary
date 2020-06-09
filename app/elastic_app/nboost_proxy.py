import logging
import requests

import qary  # noqa
from qary.skills.qa_bots import Bot

from elastic_app.constants import ES_HOST, ES_PORT, ES_INDEX
from elastic_app.es_qa import sorted_dicts

BOT_PERSONALITIES = ['qa']  # 'glossary,faq'.split(',')

QABOT = Bot()

log = logging.getLogger(__name__)

CLIENT = None


def rerank(query, host=ES_HOST, port=ES_PORT, index=ES_INDEX):
    response = requests.get(
        url=f'http://nboost:8000/{ES_INDEX}/_search',
        json={
            'nboost': {
                'uhost': 'es',
                'uport': port,
                'query_path': 'body.query.match.text',
                'topk_path': 'body.size',
                'default_topk': 10,
                'topn': 50,
                'choices_path': 'body.hits.hits',
                'cvalues_path': '_source.text'
            },
            'size': 5,
            'query': {
                'match': {'text': query}
            }
        }
    )

    return response.json()


def answers_with_nboost(statement, index=ES_INDEX, host=ES_HOST, port=ES_PORT, timeout=100, max_docs=50, max_sections=10):
    """ Query Elasticsearch using statement as query string and format results as list of 8-tuples """
    global QABOT
    query_results = rerank(query=statement)
    results = []
    for i, doc in enumerate(query_results.get('hits', {}).get('hits', {})):
        hit = doc.get('_source', {})
        hit['score'] = round(doc.get('_score', float(0)), 2)
        nboost_score = query_results.get('nboost', None).get('scores', [])[i]
        hit['nboost_score'] = round(nboost_score, 2)
        try:
            log.warning(f'QABOT.context after reset: {QABOT.context}')
            context = hit.get('text', '')
            bot_reply = QABOT.reply(statement, context=context)
            hit['reply'] = bot_reply[0][1]
            hit['reply_score'] = bot_reply[0][0]
        except Exception as e:
            hit['reply'] = ''
            hit['reply_score'] = float(0)
            log.error(f'reset_context or .reply failed: {e}')
            pass
        results.append(hit)

    # results = sorted_dicts(results, key='nboost_score', reverse=True)
    return results
