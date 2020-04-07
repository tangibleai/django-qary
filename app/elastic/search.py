from elasticsearch import Elasticsearch 

def search(index = '', text="coronavirus"):  

    client = Elasticsearch("elasticsearch:9200")
    # client = Elasticsearch("localhost:9200")

    body = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"title": {
                        'query': text,
                        "boost":3
                    }}},
                    {
                        "nested": {
                            "path": "text",
                            "query": {
                                "bool": {
                                    "should": [
                                        {"term": { "text.section_num": 0 }},
                                        { "match": { "text.section_content":  text }}
                                    ]
                                }
                            },
                            "inner_hits":{
                                "highlight": {
                                    "fields": {"text.section_content": {"number_of_fragments" : 3, 'order': "score"}}
                                }
                            }
                        }
                    }
                    
                ]
            }
        }
    }


    """ Full text search within an ElasticSearch index (''=all indexes) for the indicated text """
    return client.search(index=index,
                         body=body)

def get_results(statement):
    query = search(text=statement)
    results = []

    for doc in query['hits']['hits']:

        for highlight in doc['inner_hits']['text']['hits']['hits']:

            try:
                snippet = ' '.join(highlight['highlight']['text.section_content']),
                # snippet.encode(encoding='UTF-8',errors='strict')
                mytuple = (doc['_source']['title'],
                            doc['_score'],
                            doc['_source']['source'],
                            snippet,
                            highlight['_source']['section_num'],
                            highlight['_source']['section_title'],
                            highlight['_score'])

                results.append(mytuple)

            except:pass

    return results

if __name__ == '__main__':  
    print(get_results("coronavirus"))

