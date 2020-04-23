import logging

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import qary
from qary.constants import DATA_DIR  # noqa
from elastic_app.es_search import search_tuples, BOT_PERSONALITIES

log = logging.getLogger(__name__)

log.warning(f"qary.__file__: {qary.__file__}")
log.warning(f"qary.constants: {qary.constants}")
log.warning(f"qary.constants.DATA_DIR: {DATA_DIR}")


def test_connection(request):
    results = search_tuples("When was Stan Lee born?")
    ser_res = JsonResponse(results, safe=False)
    return HttpResponse(ser_res, content_type='application/json')


def search_index(request):

    results = []
    question = ""
    personalities = BOT_PERSONALITIES

    if request.GET.get('query'):
        question = request.GET['query']
    personalities = request.GET.get('personalities', BOT_PERSONALITIES)

    results = search_tuples(question)
    context = {
        'results': results,
        'personalities': personalities,
    }
    return render(request, 'elastic_app.html', context)


def search_qa(request):

    results = []
    question = ""

    if request.GET.get('query'):
        question = request.GET['query']

    results = search_tuples(question)
    context = {
        'results': results,
        'personalities': BOT_PERSONALITIES
    }
    return render(request, 'elastic_app.html', context)


def qa_index(request):

    results = []
    question = request.GET.get('question', "")

    results = search_tuples(text=question, index='')
    context = {'results': results}

    return render(request, 'elastic_app.html', context)
