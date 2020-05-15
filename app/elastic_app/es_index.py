# import os
import time
import logging
import pandas as pd

from elasticsearch import Elasticsearch
from elastic_app.constants import ES_HOST, ES_PORT, ES_INDEX, CACHE

# import qary  # noqa
# from qary.skills.qa_bots import Bot

log = logging.getLogger(__name__)


def denorm_index(filedir=CACHE, index=ES_INDEX, host=ES_HOST, port=ES_PORT):

    client = Elasticsearch(f"{host}:{port}")
    unpickled_df = pd.read_pickle(filedir)
    articles = unpickled_df.to_dict('records')

    for article in articles:
        try:
            client.index(index=index, body=article)
        except Exception as err:
            pageid = article.get('page_id', "key page_id not found")
            log.error(f'Failed to add the article with page ID {pageid} to {index}', err)
