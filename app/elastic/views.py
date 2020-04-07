from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .search import get_results
from elasticsearch import Elasticsearch
import requests

# Create your views here.

def index(request):
    return HttpResponse("<em>Elasticsearch project improved!</em>")

def test_connection(request):
    results = get_results("When was stan Lee born?")
    ser_res = JsonResponse(results, safe = False)
    return HttpResponse(ser_res, content_type = 'application/json')

def search_index(request):

    results = []
    question =""

    if request.GET.get('query'):
        question = request.GET['query']
    
    results = get_results(question)
    context = {'results': results}

    return render(request, 'elastic.html', context)