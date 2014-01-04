import betamax
import github3
import os
import unittest


class IntegrationHelper(unittest.TestCase):
    def setUp(self):
        self.user = os.environ.get('GH_USER', 'foo')
        self.password = os.environ.get('GH_PASSWORD', 'bar')
        self.token = os.environ.get('GH_AUTH', 'x' * 20)
        self.gh = self.get_client()
        self.session = self.gh._session
        self.recorder = betamax.Betamax(self.session)

    def get_client(self):
        return github3.GitHub()

    def token_login(self):
        self.gh.login(token=self.token)

    def basic_login(self):
        self.gh.login(self.user, self.password)

    def cassette_name(self, method, cls=None):
        class_name = cls or self.described_class
        return '_'.join([class_name, method])

    @property
    def described_class(self):
        class_name = self.__class__.__name__
        return class_name[4:]
