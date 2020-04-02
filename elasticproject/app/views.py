from django.shortcuts import render
from django.http import HttpResponse
from .search import get_results


# # Create your views here.

def index(request):
    return HttpResponse("<em>Elasticsearch project</em>")

def search_index(request):
    results = []
    question =""

    if request.GET.get('query'):
        question = request.GET['query']
    
    results = get_results(question)
    context = {'results': results,
                'count': len(results),
                'search_term': question}
    return render(request, 'elasticapp/index.html', context)
    # return render(request, 'elasticapp/index.html', context)


# def articles(request):

#     query = request.GET.get('q', '')
#     results = ArticleDocument.search().query("multi_match", query = query\
#         , fields = ["name", "title", "abstract", "description"])
#     # sqs_tag = TagDocument.search().query("match", name = query)
#     return results.to_queryset()
#     # tag = sqs_tag.to_queryset()


# from django_elasticsearch_dsl_drf.constants import (
#     LOOKUP_FILTER_RANGE,
#     LOOKUP_QUERY_IN,
#     LOOKUP_QUERY_GT,
#     LOOKUP_QUERY_GTE,
#     LOOKUP_QUERY_LT,
#     LOOKUP_QUERY_LTE,
# )
# from django_elasticsearch_dsl_drf.filter_backends import (
#     FilteringFilterBackend,
#     OrderingFilterBackend,
#     DefaultOrderingFilterBackend,
#     SearchFilterBackend,
# )
# from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
 
# from elasticapp import documents as articles_documents
# from elasticapp import serializers as articles_serializers  

# class ArticleViewSet(DocumentViewSet):
#     document = articles_documents.ArticleDocument
#     serializer_class = articles_serializers.ArticleDocumentSerializer
 
#     lookup_field = 'id'
#     filter_backends = [
#         FilteringFilterBackend,
#         OrderingFilterBackend,
#         DefaultOrderingFilterBackend,
#         SearchFilterBackend,
#     ]
 
#     # Define search fields
#     search_fields = (
#         'title',
#         'body',
#     )
 
#     # Filter fields
#     filter_fields = {
#         'id': {
#             'field': 'id',
#             'lookups': [
#                 LOOKUP_FILTER_RANGE,
#                 LOOKUP_QUERY_IN,
#                 LOOKUP_QUERY_GT,
#                 LOOKUP_QUERY_GTE,
#                 LOOKUP_QUERY_LT,
#                 LOOKUP_QUERY_LTE,
#             ],
#         },
#         'title': 'title.raw',
#         'body': 'body.raw',
#         'author': {
#             'field': 'author_id',
#             'lookups': [
#                 LOOKUP_QUERY_IN,
#             ]
#         },
#         'created': 'created',
#         'modified': 'modified',
#         'pub_date': 'pub_date',
#     }
 
#     # Define ordering fields
#     ordering_fields = {
#         'id': 'id',
#         'title': 'title.raw',
#         'author': 'author_id',
#         'created': 'created',
#         'modified': 'modified',
#         'pub_date': 'pub_date',
#     }

#     # Specify default ordering
#     ordering = ('id', 'created',)   

