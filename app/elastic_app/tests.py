from django.test import TestCase
import doctest

import elastic_app.es_search


DOCTEST_KWARGS = dict(
    optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE,
    verbose=True)


# es_search.py doctests
class ESSearchTest(TestCase):

    def test_es_search_with_djtc(self):
        results = doctest.testmod(elastic_app.es_search, **DOCTEST_KWARGS)
        self.assertGreater(results.attempted, 0)
        self.assertLess(results.failed, 1)
