#!/usr/bin/env python
""" Add documents from en.wikipedia.org to an index called "wikipedia" """
import logging

from elastic_app.constants import ES_CATEGORIES, ES_SCHEMA
from elastic_app.es_search import search
from elastic_app.es_index import search_insert_wiki

log = logging.getLogger(__name__)

if __name__ == "__main__":
    hits = search("When was Barack Obama inaugurated?").get('hits', {}).get('hits', [])
    if not len(hits):
        search_insert_wiki(categories=ES_CATEGORIES, mapping=ES_SCHEMA)
        hits = search("When was Barack Obama inaugurated?").get('hits', {}).get('hits', [])
    for doc in hits:
        for s in doc['_source'].values():
            log.info(s)
