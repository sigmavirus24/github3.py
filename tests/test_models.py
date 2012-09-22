from .base import BaseTest, expect, str_test
from github3.models import GitHubError
from requests.models import Response

try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO

from json import dumps


class TestGitHubError(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestGitHubError, self).__init__(methodName)
        self.request = Response()
        self.request.status_code = 401
        self.request.encoding = 'utf-8'
        self.json = {
            'message': 'Requires authentication',
            'errors': ['Bad credentials', 'Login is not real']
            }
        json = dumps(self.json)
        self.request.raw = StringIO(json.encode())
        self.error = GitHubError(self.request)

    def test_error(self):
        expect(self.error).isinstance(GitHubError)
        expect(repr(self.error)) != ''

    def test_code(self):
        expect(self.error.code) == 401

    def test_response(self):
        expect(self.error.response) == self.request

    def test_message(self):
        expect(self.error.message) == self.json['message']

    def test_errors(self):
        expect(self.error.errors).list_of(str_test)
