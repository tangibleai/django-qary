import logging

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import qary
from qary.constants import DATA_DIR  # noqa
from elastic_app.es_search import find_snippets, find_answers  # , BOT_PERSONALITIES

log = logging.getLogger(__name__)

log.warning(f"qary.__file__: {qary.__file__}")
log.warning(f"qary.constants: {qary.constants}")
log.warning(f"qary.constants.DATA_DIR: {DATA_DIR}")


def test_connection(request):
    results = find_snippets("When was Stan Lee born?")
    ser_res = JsonResponse(results, safe=False)
    return HttpResponse(ser_res, content_type='application/json')


def search_index(request):

    results = []
    question = ""
    personalities = []  # BOT_PERSONALITIES

    if request.GET.get('query'):
        question = request.GET['query']
    personalities = request.GET.get('personalities', personalities)

    results = find_snippets(question)
    context = {
        'results': results,
        'personalities': personalities,
    }
    return render(request, 'elastic_app.html', context)


def answers_index(request):

    results = []
    question = ""
    personalities = ['qa']  # BOT_PERSONALITIES

    if request.GET.get('query'):
        question = request.GET['query']

    results = find_answers(question)
    context = {
        'results': results,
        'personalities': personalities
    }
    return render(request, 'elastic_app.html', context)
