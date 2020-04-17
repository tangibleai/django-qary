#!/usr/bin/env python
""" Add documents from en.wikipedia.org to an index called "wikipedia" """
import logging

from elastic_app.constants import ES_CATEGORIES, ES_SCHEMA
from elastic_app.es_search import search
from elastic_app.es_index import search_insert_wiki

from elasticsearch.exceptions import NotFoundError

log = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        results = search(text="When was Barack Obama inaugurated?", index='')
    except NotFoundError:
        log.warn('No indexexes found.')
    if results is None or not len(results) or not len(results.get('hits', {}).get('hits', [])):
        search_insert_wiki(categories=ES_CATEGORIES, mapping=ES_SCHEMA)
        hits = search(text="When was Barack Obama inaugurated?", index='').get('hits', {}).get('hits', [])
        # curl -XPOST 'http://localhost:9200/wikipedia/tweet/' -d '{
        #     "user" : "kimchy",
        #     "post_date" : "2009-11-15T14:12:12",
        #     "message" : "trying out Elasticsearch"
        # }'

    for doc in hits:
        for s in doc['_source'].values():
            log.info(s)
