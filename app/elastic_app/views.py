import logging

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .es_search import search_tuples
# from elasticsearch import Elasticsearch
# import requests
import qary

log = logging.warn(f"qary.__file__: {qary.__file__}")

# log = logging.warn(f"qary.constants: {qary.constants}")

from qary.constants import DATA_DIR  # noqa
log = logging.warn(f"qary.constants.DATA_DIR: {DATA_DIR}")

# from qary import clibot  # noqa

# log = logging.warn(f"qary.clibot.__file__: {clibot.__file__}")

# Create your views here.

# BOT = clibot.CLIBot(bots=['glossary'])


def index(request):
    return HttpResponse("<em>Elasticsearch project improved!</em>")


def test_connection(request):
    results = search_tuples("When was stan Lee born?")
    ser_res = JsonResponse(results, safe=False)
    return HttpResponse(ser_res, content_type='application/json')


def search_index(request):

    results = []
    question = ""

    if request.GET.get('query'):
        question = request.GET['query']

    results = search_tuples(question)
    context = {'results': results}  # , 'reply': BOT.reply('what is an allele?')}

    return render(request, 'elastic_app.html', context)


def qa_index(request):

    results = []
    question = request.GET.get('question', "")

    results = search_tuples(text=question, index='')
    context = {'results': results}  # , 'reply': BOT.reply('what is an allele?')}

    return render(request, 'elastic_app.html', context)
