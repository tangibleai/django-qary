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
...            text=content, references=references, index='wikipedia')

"""
import logging

import wikipediaapi
from elasticsearch.exceptions import NotFoundError

from .es_search import search_hits, connect_and_ping, CLIENT
from .constants import ES_SCHEMA, ES_CATEGORIES, ES_INDEX, ES_HOST, ES_PORT

log = logging.getLogger(__name__)


def count_duplicates(client=None, page_id=None, index=''):
    """ Check if the article (page_id) already exists in the database returning a total count """
    if page_id is None:
        log.error('page_id cannot be None')
        return None
    if not client:
        client = connect_and_ping()
        return None
    try:
        return client.search(
            index=index,
            body={"query":
                  {"match":
                   {"page_id": page_id}
                   }})['hits']['total']['value']
    except NotFoundError as err:
        log.warn(f"{err}: Page_id '{page_id}' not found in index '{index}', or index does not exist.")
    return None


def insert_article(client, page, index=ES_INDEX):
    """ Add a new document to the index """
    client = client or connect_and_ping()
    section_dicts = parse_article(page)
    references = get_references(section_dicts)
    query_body = dict(title=page.title.strip(),
                      page_id=page.pageid,
                      source=page.fullurl,
                      text=page.content,
                      references=references,
                      index=index)

    if not count_duplicates(page.pageid):
        log.warning(f"page_id: '{page.pageid}'\n    is not in index: '{index}'\n"
                    f"    so adding it title: '{page.title}'")
        try:
            client.index(index=index, body=query_body)
            log.info(f"Successfully added document '{page.title}' to index {index}.")
        except Exception as error:
            log.error(f"Error writing document page_id={page.pageid}:'{page.title}':\n    {error}")

    else:
        log.info(f"Article {page.title} is already in the database index {index}")


class Document:

    def __init__(self, page):
        self.title = page.title
        self.page_id = page.pageid
        self.source = page.fullurl
        self.text = page.text
        self.sections = parse_article(page)
        self.references = get_references(self.sections)


def parse_article(page):
    """ Parse full wikipedia article into sections:

    - content sections (summary, History, Applications, etc.)
    - reference section (References, Bibliography, See Also, Notes, etc)

    TODO: use sections within page instance from wikipediaapi? improve parsing regex?

    Returns:
        sections = {'section_num': 0, 'section_title': "Summary",
        'section_content': text.split(f"\n\n{title}")[-1]}
    """

    text = page.text
    # get section titles for the existing sections
    section_titles = [sec.title for sec in page.sections]

    # initiate the sections dictionary with a summary (0th section)
    sections = [{'section_num': 0,
                 'section_title': "Summary",
                 'section_content': page.summary}]

    for i, title in enumerate(section_titles[::-1]):

        num = len(section_titles) - i
        if len(text.split(f"\n\n{title}")) == 2:
            section_dict = {"section_num": num,
                            "section_title": title,
                            "section_content": text.split(f"\n\n{title}")[-1]}
            sections.append(section_dict)
            text = text.split(f"\n\n{title}")[0]
        else:
            log.info(f"Skipping section {title} (empty section).")
            pass

    return sections


def get_references(section_dicts):
    """ Get reference sections' headers """
    reference_list = []
    content_list = []

    WIKI_REFERENCE_SECTION_TITLES = tuple('see also,references,external,links,bibliography,notes'.split())
    for d in section_dicts:
        if d['section_title'].lower().strip() in WIKI_REFERENCE_SECTION_TITLES:
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

    client = connect_and_ping(host=host, port=port)
    # exponential backoff for about a miniute to connect

    pageids_indexed = {}
    for cat in categories:
        pageids_indexed[cat] = []
        log.warning(f"Downloading Wikipedia Articles for Category:{cat}")
        try:
            cat = wiki_wiki.page(f"Category:{cat}")
        except Exception as err:
            log.error(f"The following exception occured while trying to retrieve wikipedia 'Category:{cat}':\n   {err}")

        # Parse and add articles in the category to database, first checking to see that the pageid doesn't already exist
        for key in cat.categorymembers.keys():
            page = wiki_wiki.page(key)
            title = page.title.strip()
            log.info(f"Found Category:{cat}\n    Title: {title}\n    Key: {key}\n")
            if not title.lower().startswith('category:'):
                log.warning(f"Adding page title {title} to index {index}")
                text = parse_article(page)
                content, references = get_references(text)
                try:
                    # doc = Document(client=client, host=host, port=port)
                    insert_article(client=client, page=page)
                    pageids_indexed[cat].append(page.pageid)
                except Exception as err:
                    log.error(f"The following exception occured while trying to retrieve wikipedia 'Category:{cat}':\n   {err}")
    return pageids_indexed


def print_search_results(statement):
    """ Search Elasticsearch for articles related to the provided statement and print them to the terminal """
    hits = search_hits(text=statement)
    print('Relevant articles from your ElasicSearch library:')
    print('===================')
    for doc in hits:
        print(doc['_source']['title'])
        print(doc['_source']['source'])
        print("----------------------")
