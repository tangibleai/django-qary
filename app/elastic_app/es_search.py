# import os
import time
import logging

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

from elastic_app.constants import ES_HOST, ES_PORT, ES_INDEX, ES_QUERY_NESTED

log = logging.getLogger(__name__)

CLIENT = None


def connect_and_ping(host=ES_HOST, port=ES_PORT, timeout=None, retry_timeout=2):
    t0 = time.time()
    global CLIENT
    log.info("Connecting to ElasticSearch server at {host}:{port} using {CLIENT}...")
    if not CLIENT:
        log.info(f"Connecting to ElasticSearch server at {host}:{port}")
        CLIENT = Elasticsearch(f'{host}:{port}')
    if CLIENT and not CLIENT.ping():
        log.error(f"Unable to find ElasticSearch server at {host}:{port}\n    Trying for {retry_timeout}s more.")
        CLIENT = Elasticsearch(f'{host}:{port}')
        time.sleep(0.98765)
        retry_timeout -= time.time() - t0
        if retry_timeout > 0:
            connect_and_ping(host=host, port=port, timeout=timeout, retry_timeout=retry_timeout)
    return CLIENT


def search(text="coronavirus", bodyfun=ES_QUERY_NESTED, index=ES_INDEX, host=ES_HOST, port=ES_PORT):
    """ Full text search within an ElasticSearch index (''=all indexes) for the indicated text """
    global CLIENT
    log.warn(f"Attempting to connect to '{host}:{port}'...")
    client = CLIENT or connect_and_ping(host=host, port=port, timeout=None, retry_timeout=0) or Elasticsearch(f'{host}:{port}')
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


def search_tuples(statement, index=ES_INDEX, host=ES_HOST, port=ES_PORT):
    """ Query Elasticsearch using statement as query string and format results as list of 8-tuples """
    query_results = search(text=statement, index=index, host=host, port=port)
    results = []
    for doc in query_results.get('hits', query_results).get('hits', query_results):
        # log.debug('str(doc)')
        # results.append(('_title', 'doc._score', '_source', 'snippet', 'section_num', 'section_title', 'snippet._score', doc))
        for highlight in doc.get('inner_hits', doc).get('text', doc).get('hits', doc).get('hits', {}):
            snippet = ' '.join(highlight.get('highlight', {}).get('text.section_content', []))
            # snippet.encode(encoding='UTF-8',errors='strict')
            mytuple = (
                doc['_source']['title'],
                doc['_score'],
                doc['_source']['source'],
                snippet,
                highlight['_source']['section_num'],
                highlight['_source']['section_title'],
                highlight['_score'],
                doc)
            results.append(dict(zip(range(len(mytuple)), mytuple)))
    return results
