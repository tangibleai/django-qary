#!/usr/bin/env python
""" Add documents from en.wikipedia.org to an index called "wikipedia" """
import logging

# from elasticsearch.exceptions import NotFoundError

from elastic_app.constants import ES_INDEX, ES_HOST
from elastic_app.es_index import denorm_index

from qary.etl.netutils import download_if_necessary

log = logging.getLogger(__name__)


if __name__ == "__main__":
    filepath = download_if_necessary('wikipedia_articles')
    log.warning(f'filepath: {filepath}, index={ES_INDEX}, host={ES_HOST}')
    denorm_index(filedir=filepath)
