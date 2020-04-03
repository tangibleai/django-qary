from django.shortcuts import render
from django.http import HttpResponse
from .search import get_results
from elasticsearch import Elasticsearch
import requests

# Create your views here.

def index(request):
    return HttpResponse("<em>Elasticsearch project improved!</em>")

def test_connection(request):
    context = requests.get('http://elasticsearch:9200')
    return HttpResponse(f"Connection status to elasticsearch container: {context.status_code}")

def search_index(request):
    results = []
    question =""

    if request.GET.get('query'):
        question = request.GET['query']
    
    results = get_results(question)
    context = {'results': results,
                'count': len(results),
                'search_term': question}
    return render(request, 'elastic.html', context)