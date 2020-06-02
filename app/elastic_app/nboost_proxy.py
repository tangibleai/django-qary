import requests
from pprint import pprint

def nboost_reranked(list_of_dicts):
    response = requests.get(
        url='http://localhost:8000/wikipedia/_search',
        json={
            'nboost': {
                'uhost': 'localhost',
                'uport': 9200,
                'query_path': 'body.query.match.passage',
                'topk_path': 'body.size',
                'default_topk': 10,
                'topn': 50,
                'choices_path': 'body.hits.hits',
                'cvalues_path': '_source.passage'
            },
            'size': 2,
            'query': {
                'match': {'passage': 'I want a Louisiana hotel with a pool'}
            }
        }
    )

    return response
