import requests
import github3
import expecter
import json
import sys
from mock import patch
from io import BytesIO
from unittest import TestCase


def generate_response(path_name, status_code=200, enc='utf-8', _iter=False,
                      **headers):
    r = requests.Response()
    r.status_code = status_code
    r.encoding = enc

    if path_name:
        if _iter:
            content = path(path_name).read().strip()
            content = '[{0}]'.format(content)
            r.raw = BytesIO(content.encode())
        elif sys.version_info > (3, 0):
            content = path(path_name).read().strip()
            r.raw = BytesIO(content.encode())
        else:
            r.raw = path(path_name)
    else:
        r.raw = BytesIO()

    if headers:
        r.headers = headers

    return r


def load(name):
    return json.load(path(name))


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
            'Expected None but got %s' % repr(self._actual)  # nopep8
        )

    def is_True(self):
        assert self._actual is True, (
            'Expected True but got %s' % repr(self._actual)  # nopep8
        )

    def is_False(self):
        assert self._actual is False, (
            'Expected False but got %s' % repr(self._actual)  # nopep8
        )

    def is_in(self, iterable):
        assert self._actual in iterable, (
            "Expected %s in %s but it wasn't" % (
                repr(self._actual), repr(iterable)
            )
        )

    def list_of(self, cls):
        for actual in self._actual:
            CustomExpecter(actual).isinstance(cls)

    @classmethod
    def githuberror(cls):
        return cls.raises(github3.GitHubError)

expect = CustomExpecter


class BaseCase(TestCase):
    def setUp(self):
        self.g = github3.GitHub()
        self.args = ()
        self.conf = {'allow_redirects': True}
        self.mock = patch.object(requests.sessions.Session, 'request')
        self.request = self.mock.start()

    def tearDown(self):
        self.mock.stop()

    def login(self):
        self.g.login('user', 'password')

    def mock_assertions(self):
        assert self.request.called is True
        conf = self.conf.copy()
        args, kwargs = self.request.call_args

        expect(self.args) == args

        if 'data' in self.conf and isinstance(self.conf['data'], dict):
            for k, v in list(self.conf['data'].items()):
                s = json.dumps({k: v})[1:-1]
                expect(s).is_in(kwargs['data'])

            del self.conf['data']

        for k in self.conf:
            expect(k).is_in(kwargs)
            expect(self.conf[k]) == kwargs[k]

        self.request.reset_mock()
        self.conf = conf


class APITestMixin(TestCase):
    def setUp(self):
        self.mock = patch('github3.api.gh', autospec=github3.GitHub)
        self.gh = self.mock.start()

    def tearDown(self):
        self.mock.stop()
