import copy
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


class CustomHeadersMatcher(betamax.BaseMatcher):
    name = 'gh3-headers'

    def on_init(self):
        self.headers_matcher = betamax.matchers.HeadersMatcher()

    def match(self, request, recorded_request):
        request = request.copy()
        recorded_request = copy.deepcopy(recorded_request)
        request.headers.pop('User-Agent', None)
        recorded_request['headers'].pop('User-Agent', None)
        request.headers.pop('Accept-Encoding', None)
        recorded_request['headers'].pop('Accept-Encoding', None)
        return self.headers_matcher.match(request, recorded_request)


betamax.Betamax.register_request_matcher(CustomHeadersMatcher)
