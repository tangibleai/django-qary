#!/usr/bin/env python
""" Add documents from en.wikipedia.org to an index called "wikipedia" """
import logging

# from elasticsearch.exceptions import NotFoundError

from elastic_app.constants import CACHE, ES_INDEX, ES_HOST, ES_PORT
# from elastic_app.es_search import search
from elastic_app.es_index import denorm_index

log = logging.getLogger(__name__)


if __name__ == "__main__":
    denorm_index(filedir=CACHE, index=ES_INDEX, host=ES_HOST, port=ES_PORT)
