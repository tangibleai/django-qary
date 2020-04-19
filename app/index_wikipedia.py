#!/usr/bin/env python
""" Add documents from en.wikipedia.org to an index called "wikipedia" """
import logging

# from elasticsearch.exceptions import NotFoundError

from elastic_app.constants import ES_CATEGORIES, ES_SCHEMA, ES_INDEX, ES_HOST, ES_PORT
# from elastic_app.es_search import search
from elastic_app.es_index import search_insert_wiki

log = logging.getLogger(__name__)


if __name__ == "__main__":
    search_insert_wiki(categories=ES_CATEGORIES, mapping=ES_SCHEMA,
                       index=ES_INDEX, host=ES_HOST, port=ES_PORT)
