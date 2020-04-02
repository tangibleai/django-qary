from elasticsearch import Elasticsearch 

def search(index = '', text="Barack Obama"):  

    client = Elasticsearch()

    """ Full text search within an ElasticSearch index (''=all indexes) for the indicated text """
    return client.search(index=index,
                         body={"query": {"match": {"text": text}}}
                         )

def search_nested(text, index=''):

    client = Elasticsearch()

    return client.search(index=index,
                        body={
                            "query": {
                                "nested":{
                                    "path":"text",
                                    "query":{
                                        "bool": {
                                        "must": [
                                            {"match":{"text.section_content":text}},
                                            {"match":{"text.section_num":0}}
                                            ]
                                        }
                                    }
                                }
                            }
                        })

def get_results(statement):
    query = search_nested(text=statement)
    results = []
    for doc in query['hits']['hits']:
        doc_tuple = (doc['_source']['title'], doc['_source']['source'])
        results.append(doc_tuple)

    return results


if __name__ == '__main__':  
    print(get_results("What are coronavirus symptoms?"))