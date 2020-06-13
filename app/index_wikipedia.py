#!/usr/bin/env python
""" Add documents from en.wikipedia.org to an index called "wikipedia" """
import logging

# from elasticsearch.exceptions import NotFoundError

from elastic_app.constants import CACHE, ES_INDEX, ES_HOST, ES_PORT
# from elastic_app.es_search import search
from elastic_app.es_index_only import denorm_index
from qary.etl import download_if_necessary


log = logging.getLogger(__name__)


if __name__ == "__main__":
    filepath = download_if_necessary('wikipedia_articles')
    denorm_index(filedir=filepath, index=ES_INDEX, host=ES_HOST, port=ES_PORT)
