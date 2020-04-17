""" Utilities for adding documents to Elasticsearch database index

$ CONTAINERID=$(docker ps | grep -E '.*django-qary_web' | cut -c -12)  # a53dbae601c8
$ docker exec -it $CONTAINERID /bin/bash

app@a53dbae601c8:~/web$ python manage.py shell

>>> from elastic_app.es_index import *
>>> client = Elasticsearch(f"{ES_HOST}:{ES_PORT}")
>>> client
<Elasticsearch([{'host': 'es', 'port': 9200}])>
>>> client.ping()
True
>>> wiki_wiki = wikipediaapi.Wikipedia('en')  # LOL Buck Rogers
>>> c = ES_CATEGORIES[0]
>>> c
'Marvel Comics'
>>> cat = wiki_wiki.page(f"Category:{c}")
>>> k = cat.categorymembers.keys()
>>> k
dict_keys(['Marvel Comics', 'Big Two Comics', 'Bullpen Bulletins', 'Heroes World Distribution', ...
>>> k = list(k)[0]
>>> k
'Marvel Comics'
>>> page = wiki_wiki.page(k)
>>> title = page.title.strip()
>>> title
'Marvel Comics'
>>> text = parse_article(page)
>>> text
[{'section_num': 0, 'section_title': 'Summary', 'sec...
>>> content, references = get_references(text)
>>> references
[{'section_num': 10,
  'section_title': 'Notes',
  'section_content': '\nReferences\nFurther reading\nExternal links\n Media related to Marvel ...
>>> content
[{'section_num': 0, 'section_title': 'Summary', 'section_content': "Marvel Comics is the brand name
>>> doc = Document()
# notice Document.page_id (from ES_SCHEMA) not Wikipedia.pageid (from wikipedia api)
>>> doc.insert(title=title, page_id=page.pageid, url=page.fullurl,
...            text=content, references=references, index=index)

"""
import time
import logging

import wikipediaapi
from slugify import slugify
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

from .es_search import search, connect_and_ping, CLIENT
from .constants import ES_SCHEMA, ES_CATEGORIES, ES_INDEX, ES_HOST, ES_PORT

log = logging.getLogger(__name__)


class Document:

    def __init__(self, title='', page_id=None, source='', text='',
                 client=None, host=ES_HOST, port=ES_PORT):
        self.client = client or connect_and_ping(host=host, port=port, retry_timeout=1.5)
        self.title = title
        self.page_id = page_id
        self.source = source
        self.text = text

        if not self.client or not self.client.ping():
            try:
                self.client = Elasticsearch(f"{host}:{port}")
            except ConnectionRefusedError:
                log.error("Failed to connect to Elasticsearch on {host}:{port}")

    def count_duplicates(self, page_id, index=''):
        """ Check if the article already exists in the database returning a total count """
        try:
            return self.client.search(
                index=index,
                body={"query":
                      {"match":
                       {"page_id": page_id}
                       }})['hits']['total']['value']
        except NotFoundError as err:
            log.warn(f"{err}: Page_id '{page_id}' not found in index '{index}', or index does not exist.")
        return None

    def insert(self, title, page_id, url='', text='', references=[], index=ES_INDEX):
        """ Add a new document to the index """

        self.title = title
        self.page_id = page_id
        self.source = url
        self.text = text
        self.references = references
        self.body = {'title': self.title,
                     'page_id': self.page_id,
                     'source': self.source,
                     'text': self.text,
                     'references': self.references}

        # wait 6 minutes for es server to come up
        if not self.count_duplicates(page_id):
            try:
                self.client.index(index=index, body=self.body)
                log.info(f'Successfully added document {self.title} to index {index}.')
            except Exception as error:
                log.error(f"Error writing document {page_id}={self.page_id}:{self.title}:\n    {error}")

        else:
            log.info(f"Article {self.title} is already in the database index {index}")


def parse_article(article):
    '''
    Parse full wikipedia article into sections:
    - content sections (summary, History, Applications, etc.)
    - reference section (References, Bibliography, See Also, Notes, etc)
    '''

    text = article.text
    # get section titles for the existing sections
    section_titles = [sec.title for sec in article.sections]

    # initiate the sections dictionary with a summary (0th section)
    sections = [{'section_num': 0,
                 'section_title': "Summary",
                 'section_content': article.summary}]

    for i, title in enumerate(section_titles[::-1]):

        num = len(section_titles) - i
        if len(text.split(f"\n\n{title}")) == 2:
            section_dict = {"section_num": num,
                            "section_title": title,
                            "section_content": text.split(f"\n\n{title}")[-1]}
            sections.append(section_dict)
            text = text.split(f"\n\n{title}")[0]
        else:
            log.info(f"Skipping section {title} (empty)S.")
            pass

    return sections


def get_references(mylist):
    '''
    Get reference sections' headers
    '''
    reference_list = []
    content_list = []

    for d in mylist:
        if d['section_title'].lower() in ' '.join(['see also references external links bibliography notes']):
            reference_list.append(d)
        else:
            content_list.append(d)

    return (content_list, reference_list)


def search_insert_wiki(categories=ES_CATEGORIES, mapping=ES_SCHEMA, index=ES_INDEX,
                       client=CLIENT, host=ES_HOST, port=ES_PORT):
    """ Retrieve all wikipedia pages associated with the categories listed in `categories`

    Input:
        categories (str or seq): sequence of strs or str with comma separated names of categories
        mapping (dict): elastic search schema (called "mapping" in Elasticsearch documentation)
    """

    wiki_wiki = wikipediaapi.Wikipedia('en')  # Nice, Buck Rogers
    if isinstance(categories, str):
        categories = [c.strip() for c in categories.split(',')]

    wiki_wiki = wikipediaapi.Wikipedia('en')  # LOL Buck Rogers

    client = connect_and_ping(client)
    for i in range(10):
        if client.ping():
            break
        log.warn(f"Can't connect to {ES_HOST}:{ES_PORT} after {i+1} attempts")
        time.sleep(0.987)
    for c in categories:
        try:
            # create empty index with predefined schema (data structure)
            # client.indices.create(index=index, body={"mappings": mapping})
            # log.info(f'New index {index} has been created')

            # Retrieve Wikipedia article with list of article urls for the category `c`'''
            cat = wiki_wiki.page(f"Category:{c}")

            # Parse and add articles in the category to database
            for key in cat.categorymembers.keys():
                page = wiki_wiki.page(key)
                title = page.title.strip()
                if not title.lower().startswith('category:'):
                    text = parse_article(page)
                    content, references = get_references(text)
                    doc = Document(client=client, host=host, port=port)
                    doc.insert(
                        title=title,
                        page_id=page.pageid,
                        url=page.fullurl,
                        text=content,
                        references=references,
                        index=index)

        except Exception as error:
            log.info(f"The following exception occured while trying to create index '{slugify(c)}': ", error)


def print_search_results(statement):
    """ Search Elasticsearch for articles related to the provided statement and print them to the terminal """
    res = search(text=statement)
    print('Relevant articles from your ElasicSearch library:')
    print('===================')
    for doc in res['hits']['hits']:
        print(doc['_source']['title'])
        print(doc['_source']['source'])
        print("----------------------")
