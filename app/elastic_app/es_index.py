import logging

import wikipediaapi
from slugify import slugify
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from search import search

from constants import ES_SCHEMA, ES_INDEX, ES_CATEGORIES


log = logging.getLogger(__name__)

try:
    client = Elasticsearch("localhost:9200")
except ConnectionRefusedError:
    log.info("Failed to launch Elstcisearch")

wiki_wiki = wikipediaapi.Wikipedia('en')


class Document:

    def __init__(self):
        self.title = ''
        self.page_id = None
        self.source = ''
        self.text = ''

    def count_duplicates(self, page_id, index=ES_INDEX):
        """ Check if the article already exists in the database returning a total count """
        try:
            return client.search(index=index,
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

        if not self.count_duplicates(page_id):

            try:
                client.index(index=index, body=self.body)
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


def search_insert_wiki(categories=ES_CATEGORIES, mapping=ES_SCHEMA):
    """ Retrieve all wikipedia pages associated with the categories listed in `categories`

    Input:
        categories (str or seq): sequence of strs or str with comma separated names of categories
        mapping (dict): elastic search schema (called "mapping" in Elasticsearch documentation)
    """
    if isinstance(categories, str):
        categories = [c.strip() for c in categories.split(',')]

    wiki_wiki = wikipediaapi.Wikipedia('en')  # LOL Buck Rogers

    for c in categories:
        try:
            # create empty index with predefined schema (data structure)
            client.indices.create(index=slugify(c), body={"mappings": mapping})
            log.info(f'New index {slugify(c)} has been created')

            # Retrieve Wikipedia article with list of article urls for the category `c`'''
            cat = wiki_wiki.page(f"Category:{c}")

            # Parse and add articles in the category to database
            for key in cat.categorymembers.keys():
                page = wiki_wiki.page(key)
                if "Category:" not in page.title:
                    text = parse_article(page)
                    content, references = get_references(text)
                    doc = Document()
                    doc.insert(page.title, page.pageid, page.fullurl, content, references, index=slugify(c))

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


if __name__ == "__main__":

    hits = search("When was Barack Obama inaugurated?").get('hits', {}).get('hits', [])
    if not len(hits):
        search_insert_wiki(categories=ES_CATEGORIES, mapping=ES_SCHEMA)
        hits = search("When was Barack Obama inaugurated?").get('hits', {}).get('hits', [])
    for doc in hits:
        for s in doc['_source'].values():
            log.info(s)
