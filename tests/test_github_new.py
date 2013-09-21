import github3
import os
import sys

if sys.version_info < (3, 0):
    from unittest2 import TestCase
else:
    from unittest import TestCase

from betamax import Betamax


class BaseCase(TestCase):
    def setUp(self):
        self.auth = os.environ.get('GH_AUTH')
        self.g = github3.GitHub()
        self.session = self.g._session

    def login(self):
        self.g.login(token=self.auth)

    def test_create_gist(self):
        self.login()
        with Betamax(self.session).use_cassette('GitHub_create_gist'):
            #import pytest; pytest.set_trace()
            g = self.g.create_gist(
                'Gist Title', {'filename.py': {'content': '#content'}}
            )

        assert isinstance(g, github3.gists.Gist)
