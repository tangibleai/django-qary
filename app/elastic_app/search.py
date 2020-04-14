import os
import logging

from elasticsearch import Elasticsearch

log = logging.getLogger(__name__)

ES_HOST = os.environ.get('ES_HOST', 'es')  # or localhost
ES_PORT = os.environ.get('ES_PORT', '9200')  # or 9200


def connect_and_ping(host=ES_HOST, port=ES_PORT, timeout=None):
    global CLIENT
    if CLIENT is not None:  # and CLIENT.ping():
        client = CLIENT
    else:
        log.info(f"Connecting to ElasticSearch server at {host}:{port}")
        client = Elasticsearch(host=ES_HOST, port='9200')
    if not client.ping():
        log.error(f"Unable to find ElasticSearch server at {host}:{port}")
    CLIENT = client
    return CLIENT


def search(index='', text="coronavirus"):
    # client = connect_and_ping()  # Elasticsearch(f'{ES_HOST}:{ES_PORT}')
    client = Elasticsearch(ES_HOST + ':9200')

    body = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"title": {
                        'query': text,
                        "boost": 3
                    }}},
                    {
                        "nested": {
                            "path": "text",
                            "query": {
                                "bool": {
                                    "should": [
                                        {"term": {"text.section_num": 0}},
                                        {"match": {"text.section_content": text}}
                                    ]
                                }
                            },
                            "inner_hits": {
                                "highlight": {
                                    "fields": {"text.section_content": {"number_of_fragments": 3, 'order': "score"}}
                                }
                            }
                        }
                    }

                ]
            }
        }
    }

    """ Full text search within an ElasticSearch index (''=all indexes) for the indicated text """
    return client.search(index=index, body=body)


def get_results(statement):
    query = search(text=statement)
    results = []

    for doc in query['hits']['hits']:

        for highlight in doc['inner_hits']['text']['hits']['hits']:

            try:
                snippet = ' '.join(highlight['highlight']['text.section_content']),
                # snippet.encode(encoding='UTF-8',errors='strict')
                mytuple = (doc['_source']['title'],
                           doc['_score'],
                           doc['_source']['source'],
                           snippet[0],
                           highlight['_source']['section_num'],
                           highlight['_source']['section_title'],
                           highlight['_score'])

                results.append(mytuple)

            except:  # noqa
                pass

    return results


if __name__ == '__main__':
    print(get_results("coronavirus"))
