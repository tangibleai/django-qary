from elasticsearch import Elasticsearch 

def search(index = '', text="Barack Obama"):  

    client = Elasticsearch('127.0.0.1:9200')

    """ Full text search within an ElasticSearch index (''=all indexes) for the indicated text """
    return client.search(index=index,
                         body={"query": {"match": {"text": text}}}
                         )

def get_results(statement):
    query = search(text=statement)
    results = []
    for doc in query['hits']['hits']:
        doc_tuple = (doc['_source']['title'], doc['_source']['source'])
        results.append(doc_tuple)

    return results


if __name__ == '__main__':  
    print(get_results("Barak Obama"))