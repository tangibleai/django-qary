import os

from elasticsearch import Elasticsearch


ES_HOST = os.environ.get("ES_HOST", "es")  # or localhost:9200
CLIENT = Elasticsearch(host=ES_HOST, port='9200')
if not CLIENT.ping():
    raise RuntimeError("Unable to find ElasticSearch server at {}:9200".format(ES_HOST))


def search(index='', text="coronavirus"):
    # client = Elasticsearch(ES_HOST)

    body = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"title": {
                        'query': text,
                        "boost": 3
                    }}},
                    {
                        "nested": {
                            "path": "text",
                            "query": {
                                "bool": {
                                    "should": [
                                        {"term": {"text.section_num": 0}},
                                        {"match": {"text.section_content": text}}
                                    ]
                                }
                            },
                            "inner_hits": {
                                "highlight": {
                                    "fields": {"text.section_content": {"number_of_fragments": 3, 'order': "score"}}
                                }
                            }
                        }
                    }

                ]
            }
        }
    }

    """ Full text search within an ElasticSearch index (''=all indexes) for the indicated text """
    return CLIENT.search(index=index, body=body)


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
                           snippet[0],
                           highlight['_source']['section_num'],
                           highlight['_source']['section_title'],
                           highlight['_score'])

                results.append(mytuple)

            except:  # noqa
                pass

    return results


if __name__ == '__main__':
    print(get_results("coronavirus"))
