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
        self.user = os.environ.get('GH_USER')
        self.password = os.environ.get('GH_PASSWORD')
        self.token = os.environ.get('GH_AUTH', 'x' * 20)
        self.g = github3.GitHub()
        self.session = self.g._session

    def login_token(self):
        self.g.login(token=self.token)

    def login_user(self):
        self.g.login(self.user, self.password)

    def test_create_gist(self):
        self.login_token()
        with Betamax(self.session).use_cassette('GitHub_create_gist'):
            g = self.g.create_gist(
                'Gist Title', {'filename.py': {'content': '#content'}}
            )

        assert isinstance(g, github3.gists.Gist)
        assert g.files == 1
        assert g.is_public() is True

    def test_create_issues(self):
        self.login_token()
        with Betamax(self.session).use_cassette('GitHub_create_issue'):
            i = self.g.create_issue(
                'github3py', 'fork_this', 'Test issue creation',
                "Let's see how well this works with Betamax"
                )

        assert isinstance(i, github3.issues.Issue)
        assert i.title == 'Test issue creation'
        assert i.body == "Let's see how well this works with Betamax"
