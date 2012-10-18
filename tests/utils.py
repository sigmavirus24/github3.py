import requests
import github3
import expecter
from mock import patch, call
from io import BytesIO
from unittest import TestCase


def generate_response(path_name, status_code=200, enc='utf-8', _iter=False):
    r = requests.Response()
    r.status_code = status_code
    r.encoding = enc
    if path_name:
        content = path(path_name).read()
        if _iter:
            content = '[{0}]'.format(content)
        r.raw = BytesIO(content.encode())
    else:
        r.raw = BytesIO()
    return r


def path(name, mode='r'):
    return open('tests/json/{0}'.format(name), mode)


def patch_request(method='request'):
    return patch.object(requests.sessions.Session, method)


class CustomExpecter(expecter.expect):
    def is_not_None(self):
        assert self._actual is not None, (
                'Expected anything but None but got it.'
                )

    def is_None(self):
        assert self._actual is None, (
                'Expected None but got %s' % repr(self._actual)
                )

    def is_True(self):
        assert self._actual is True, (
                'Expected True but got %s' % repr(self._actual)
                )

    def is_False(self):
        assert self._actual is False, (
                'Expected False but got %s' % repr(self._actual)
                )

    def list_of(self, cls):
        for actual in self._actual:
            CustomExpecter(actual).isinstance(cls)

    def githuberror(self):
        return self.raises(github3.GitHubError)

expect = CustomExpecter


class BaseCase(TestCase):
    def setUp(self):
        self.g = github3.GitHub()
        self.request = patch_request()
        self.request.start()

    def tearDown(self):
        self.request.stop()

    def login(self):
        self.g.login('user', 'password')
        self.conf = {'allow_redirects': True}

    def mock_assertions(self, *args, **kwargs):
        assert self.request.called is True
        assert call(*args, **kwargs) in self.request.mock_calls
