import os


ES_HOST = os.environ.get('ES_HOST', 'es')  # or localhost
ES_PORT = os.environ.get('ES_PORT', '9200')  # or 9200
ES_INDEX = 'wikipedia'


ES_CATEGORIES = (
    'Marvel Comics',
    'Machine learning',
    'Marvel Comics editors-in-chief',
    'American science fiction television series',
    'Science fiction television',
    'Natural language processing',
    'American comics writers',
    'Presidents of the United States',
    'Coronaviridae',
    'Pandemics',
)


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
