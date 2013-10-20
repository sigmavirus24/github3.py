import betamax
import github3
import os
import sys

if sys.version_info < (3, 0):
    from unittest2 import TestCase
else:
    from unittest import TestCase


class IntegrationHelper(TestCase):
    def setUp(self):
        self.user = os.environ.get('GH_USER')
        self.password = os.environ.get('GH_PASSWORD')
        self.token = os.environ.get('GH_AUTH', 'x' * 20)
        self.gh = github3.GitHub()
        self.session = self.gh._session
        self.recorder = betamax.Betamax(self.session)

    def token_login(self):
        self.gh.login(token=self.token)

    def basic_login(self):
        self.gh.login(self.user, self.password)

    def cassette_name(self, method):
        class_name = self.described_class
        return '_'.join([class_name, method])

    @property
    def described_class(self):
        class_name = self.__class__.__name__
        return class_name[4:]
