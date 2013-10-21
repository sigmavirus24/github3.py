import json
import os
import sys

if sys.version_info < (3, 0):
    from unittest2 import TestCase
else:
    from unittest import TestCase

import requests
import github3
from mock import patch
from io import BytesIO
from requests.structures import CaseInsensitiveDict

is_py3 = sys.version_info > (3, 0)


def load(name):
    with path(name) as f:
        j = json.load(f)
    return j


def path(name, mode='r'):
    return open('tests/json/{0}'.format(name), mode)


class BaseCase(TestCase):
    github_url = 'https://api.github.com/'

    def setUp(self):
        self.g = github3.GitHub()
        self.session = self.g._session
        if os.environ.get('GH_AUTH'):
            self.g.login(token=os.environ['GH_AUTH'])
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

        assert self.args == args

        if 'data' in self.conf:
            if isinstance(self.conf['data'], dict):
                for k, v in list(self.conf['data'].items()):
                    s = json.dumps({k: v})[1:-1]
                    assert s in kwargs['data']
            else:
                assert self.conf['data'] == kwargs['data']

            del self.conf['data']

        for k in self.conf:
            assert k in kwargs
            assert self.conf[k] == kwargs[k]

        self.request.reset_mock()
        self.conf = conf

    def response(self, path_name, status_code=200, enc='utf-8',
                 _iter=False, **headers):
        r = requests.Response()
        r.status_code = status_code
        r.encoding = enc

        if path_name:
            with path(path_name) as f:
                content = f.read().strip()

            if _iter:
                content = '[{0}]'.format(content)
                r.raw = RequestsBytesIO(content.encode())
            elif is_py3:
                r.raw = RequestsBytesIO(content.encode())
            else:
                r.raw = RequestsBytesIO(content)
        else:
            r.raw = RequestsBytesIO()

        if headers:
            r.headers = CaseInsensitiveDict(headers)

        self.request.return_value = r

    def delete(self, url):
        self.args = ('DELETE', url)
        self.conf = {}

    def get(self, url):
        self.args = ('GET', url)

    def patch(self, url):
        self.args = ('PATCH', url)

    def post(self, url):
        self.args = ('POST', url)

    def put(self, url):
        self.args = ('PUT', url)

    def not_called(self):
        assert self.request.called is False

    def assertGitHubErrorRaised(self, func, *args, **kwargs):
        return self.assertRaises(github3.GitHubError, func(*args, **kwargs))


class RequestsBytesIO(BytesIO):
    def read(self, chunk_size, *args, **kwargs):
        return super(RequestsBytesIO, self).read(chunk_size)
