# import os
import logging

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

from .constants import ES_HOST, ES_PORT, ES_INDEX

log = logging.getLogger(__name__)

CLIENT = None


def connect_and_ping(host=ES_HOST, port=ES_PORT, timeout=None):
    global CLIENT
    if CLIENT:
        client = CLIENT
    else:
        log.info(f"Connecting to ElasticSearch server at {host}:{port}")
        client = Elasticsearch(host=host, port=port)
    if not client.ping():
        log.error(f"Unable to find ElasticSearch server at {host}:{port}")
    CLIENT = client
    return CLIENT


def search(text="coronavirus", index=ES_INDEX, host=ES_HOST, port=ES_PORT):
    # client = connect_and_ping()  # Elasticsearch(f'{host}:{port}')
    log.warn(f"Attempting to connect to '{host}:{port}'...")
    client = Elasticsearch(f'{host}:{port}')
    log.warn(f"Attempting to ping '{client}'...")
    if not client.ping():
        log.error(f"Unable to find ElasticSearch server at {host}:{port} using {client}")
    log.warn(f"Attempting to search for text='{text}'\n in index='{index}'\n")
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
    try:
        return client.search(body=body, index=index)
    except NotFoundError as e:
        log.error(f"{e}:\n    Unable to find any records on {host}:{port}, "
                  "perhaps because there is no index named '{index}'")
        return {}


def get_results(statement):
    query_results = search(text=statement)
    results = []

    for doc in query_results.get('hits', query_results).get('hits', query_results):

        for highlight in doc.get('inner_hits', doc).get('text', doc).get('hits', doc).get('hits', {}):

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
