import wikipediaapi
from slugify import slugify
from elasticsearch import Elasticsearch 
from search import search

try:
    client = Elasticsearch("localhost:9200")
except ConnectionRefusedError:
    print("Failed to launch Elstcisearch")

wiki_wiki = wikipediaapi.Wikipedia('en')

mapping = {
    "properties": {
        
            "text": {
                "type": "nested",
                "properties":{
                    "section_num": {"type":"integer"},
                    "section_title": {"type":"text"},
                    "section_content": {"type":"text"}
                }
            },
        
            "references": {
                "type": "nested",
                "properties":{
                    "section_num": {"type":"integer"},
                    "section_title": {"type":"text"},
                    "section_content": {"type":"text"}
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

class Document:
    
    def __init__(self):
        self.title = ''
        self.page_id = None
        self.source = ''
        self.text = ''
        
    def __if_exists(self, page_id, index=""):
        '''
        Check if the article already exists in the database
        with a goal to avoid duplication
        '''
        
        return client.search(index=index, 
                             body={"query": 
                                   {"match": 
                                    {"page_id": page_id}
                                   }})['hits']['total']['value']
        
    def insert(self, title, page_id, url, text, references, index):
        ''' Add a new document to the index'''
        
        self.title=title
        self.page_id=page_id
        self.source=url
        self.text=text
        self.references = references
        self.body = {'title': self.title,
            'page_id': self.page_id,
            'source':self.source,
            'text': self.text,
            'references':self.references}
        
        if self.__if_exists(page_id) == 0:
        
            try:
                client.index(index=index, body=self.body)
                print(f'Successfully added document {self.title} to index {index}.')
            except Exception as error:
                print(f"Error writing document {page_id}: {error}")
                
        else:
            print(f"Article {self.title} is already in the database")


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

        num = len(section_titles)-i
        if len(text.split(f"\n\n{title}")) == 2:
            section_dict = {"section_num": num,
                            "section_title": title,
                            "section_content": text.split(f"\n\n{title}")[-1]}
            sections.append(section_dict)
            text = text.split(f"\n\n{title}")[0]
        else:
            print(f"Skipping section {title} (empty)S.")
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


def search_insert_wiki(category, mapping):
    
    if type(category) is not list: category = [ category ]

    wiki_wiki = wikipediaapi.Wikipedia('en')
    
    for c in category:
        
        try:
                    
            '''Create and empty index with predefined data structure'''
            client.indices.create(index=slugify(c), body={"mappings":mapping})
            print(f'New index {slugify(c)} has been created')
            
            '''Access the list of wikipedia articles in category c'''
            cat = wiki_wiki.page(f"Category:{c}")
            
            ''' Parse and add articles in the category to database'''
            for key in cat.categorymembers.keys():
                page = wiki_wiki.page(key)

                if not "Category:" in page.title:

                    text = parse_article(page)
                    content, references = get_references(text)
                    doc = Document()
                    doc.insert(page.title, page.pageid, page.fullurl, content, references, index=slugify(c))


        except Exception as error:
            print(f"The following exception occured while trying to create index '{slugify(c)}': ", error)


def test_search(statement):
    res = search(text=statement)
    print('Relevant articles from your ElasicSearch library:')
    print('===================')
    for doc in res['hits']['hits']:
        print(doc['_source']['title'])
        print(doc['_source']['source'])
        print("----------------------")

def test_index(category):
    search_insert_wiki(category, mapping=mapping)


if __name__=="__main__":
    
    # test_index('American science fiction television series')
    test_search("when barack obama was inaugurated?")

    # To add new categories to elasticsearch:
    # categories = ['Marvel Comics',
    #             'Machine learning',
    #             'Marvel Comics editors-in-chief',
    #             'American science fiction television series',
    #             'Science fiction television',
    #             'Natural language processing',
    #             'American comics writers', 
    #             'Presidents of the United States',
    #             'Coronaviridae',
    #             'Pandemics'
    #             ]
    
    # search_insert_wiki(categories, mapping)