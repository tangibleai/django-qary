import os
import logging

log = logging.getLogger(__name__)


ES_HOST = os.environ.get('ES_HOST', 'es').strip()  # or localhost
ES_PORT = os.environ.get('ES_PORT', '9200')  # or 9200
ES_INDEX = 'wikipedia'
CACHE = '/home/olesya/code/chatbot/django-qary/scripts/docs/articles_with_keywords.pkl'

try:
    ES_PORT = int(ES_PORT)
except ValueError:
    log.error(f"Invalid port number for ES_PORT: {ES_PORT}")
    ES_PORT = 9200


# default categories to index in Elasticsearch
# values are some representative page IDs in each category
# The first page ID, plus a middling value and the max value for id
ES_CATEGORIES = {
    'Marvel Comics': (),
    'Machine learning': (),
    'Marvel Comics editors-in-chief': (),
    'American science fiction television series': (),
    'Science fiction television': (),
    'Natural language processing': (),
    'American comics writers': (),
    'Presidents of the United States': (),
    'Barak Obama': (534366, 21870933, 63211582),
    'Coronaviridae': (),
    'Pandemics': (),
}


ES_SCHEMA = {
    "properties": {

        "text": {
            "type": "nested",
            "properties": {
                    "section_num": {"type": "integer"},
                    "section_title": {"type": "text"},
                    "section_content": {"type": "text"}
            }
        },

        "references": {
            "type": "nested",
            "properties": {
                    "section_num": {"type": "integer"},
                    "section_title": {"type": "text"},
                    "section_content": {"type": "text"}
            }
        },

        "title": {
            "type": "text"
        },

        "source": {
            "type": "text"
        },

        "page_id": {
            "type": "long"
        },

    }
}


def ES_QUERY_ALL(query):
    return {"query": {"bool": {"must": {"query_string": {"query": query}}}}}


def ES_QUERY_TITLE(query):
    return {"query": {"bool": {"should": [{"match": {"title": {'query': query, "boost": 3}}}]}}}


def ES_QUERY_TITLE_TEXT(query):
    return {"query": {"bool": {"must": {"query_string": {"query": query}},
                               "should": [{"match": {"title": {'query': query, "boost": 3}}}]}}}


def ES_QUERY_TITLE_TEXT_HIGHLIGHT_WIP(query):
    return {"query": {"bool": {"must": {"query_string": {"query": query}},
                               "should": [{"match": {"title": {'query': query, "boost": 3}}}]}}}


def ES_QUERY_NESTED(query):
    return {"query": {"bool": {"should": [{"match": {"title": {'query': query, "boost": 3}}},
                                          {"nested": {"path": "text", "query":
                                                      {"bool": {"should": [{"term": {"text.section_num": 0}},
                                                                           {"match": {"text.section_content": query}}]}},
                                                      "inner_hits": {"highlight":
                                                                     {"fields": {"text.section_content":
                                                                                 {"number_of_fragments": 3, 'order': "score"}}}}}}]
                               }
                      }
            }


def ES_QUERY_NESTED_UNIFIED(query):
    return {"query": {"bool": {"should": [{"match": {"title": {'query': query, "boost": 3}}},
                                          {"nested": {"path": "text", "query":
                                                      {"bool": {"should": [{"term": {"text.section_num": 0}},
                                                                           {"match": {"text.section_content": query}}]}},
                                                      "inner_hits": {"highlight":
                                                                     {"fields": {"text.section_content":
                                                                                 {"number_of_fragments": 1,
                                                                                  "fragment_size": 512,
                                                                                  'order': "score"}}}}}}]
                               }
                      }
            }


def ES_QUERY_BROKE(query):
    return {"query": {"bool": {"should": [{"match": {"title": {'query': query, "boost": 3}}},
                                          {"nested": {"path": "text", "query":
                                                      {"bool": {"should": [{"term": {"text.section_num": 0}},
                                                                           {"match": {"text.section_content": query}}]}},
                                                      "inner_hits": {"highlight":
                                                                     {"fields": {"text.section_content":
                                                                                 {"number_of_fragments": 3, 'order': "score"}}}}}}]
                               }
                      }
            }


def ES_QUERY_FLAT(query):
    return {"query": {"bool": {"must_not": [{"term": {"section_title": "lists"}},
                                            {"term": {"section_title": "links"}},
                                            {"term": {"section_title": "other"}},
                                            {"term": {"section_title": "bibliography"}},
                                            {"term": {"section_title": "references"}},
                                            {"term": {"section_title": "official"}},
                                            ],
                               "should": [{"multi_match": {"query": query, "fields": ["keywords^3", "text"]}}]}},
            "highlight": {"fields": {"text": {"number_of_fragments": 3, 'order': "score", "fragment_size": 512}}}}


def ES_QUERY_FLAT_STRING(query):
    return {"query": {"query_string": {"query": query, "default_field": "text"}},
            "highlight": {"fields": {"text": {"number_of_fragments": 3, 'order': "score", "fragment_size": 512}}}}


def ES_QUERY_FLAT_SIMPLE_STRING(query):
    return {"query": {"simple_query_string": {
                      "query": query,
                      "fields": ["keywords^5", "text"],
                      "auto_generate_synonyms_phrase_query": False}},
            "highlight": {"fields": {"text": {"number_of_fragments": 3, 'order': "score", "fragment_size": 512}}}}
