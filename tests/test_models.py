from .base import BaseTest, expect, str_test
import github3
from requests.models import Response

try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO

from json import dumps


class TestGitHubError(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestGitHubError, self).__init__(methodName)
        self.request = self._build_response_(True)
        self.error = github3.GitHubError(self.request)

        self.request2 = self._build_response_()
        self.error2 = github3.GitHubError(self.request2)

    def _build_json_(self, with_errors=False):
        json = {'message': 'Requires authentication'}
        if with_errors:
            json['errors'] = ['Bad credentials', 'Login is not real']
        return json

    def _build_response_(self, with_errors=False):
        r = Response()
        r.status_code = 401
        r.encoding = 'utf-8'
        json = dumps(self._build_json_(with_errors))
        r.raw = StringIO(json.encode())
        return r

    def test_error(self):
        expect(repr(self.error)) != ''
        expect(str(self.error)) != ''
        expect(str(self.error2)) != ''

    def test_code(self):
        expect(self.error.code) == 401

    def test_response(self):
        expect(self.error.response) == self.request

    def test_message(self):
        json = self._build_json_()
        expect(self.error.message) == json['message']

    def test_errors(self):
        expect(self.error.errors).list_of(str_test)

    def test_str(self):
        expect(str(self.error)) == '401 Requires authentication'


class TestBaseComment(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestBaseComment, self).__init__(methodName)
        g = github3.GitHub()
        g._session.auth = True
        self.comment = github3.models.BaseComment({}, g)

    def test_edit(self):
        expect(self.comment.edit(None)).is_False()


class TestBaseAccount(BaseTest):
    def __init__(self, methodName='runTest'):
        super(TestBaseAccount, self).__init__(methodName)
        self.account = github3.models.BaseAccount({'type': 'base'}, None)

    def test_repr(self):
        expect(repr(self.account)) != ''

    def test_update(self):
        self.account._update_({'type': 'base'})


class TestFromJSON(BaseTest):
    def test_account_from_json(self):
        b = github3.models.BaseAccount.from_json({'type': 'base'})
        expect(b).isinstance(github3.models.BaseAccount)

    def test_core_from_json(self):
        c = github3.models.GitHubObject.from_json({})
        expect(c).isinstance(github3.models.GitHubObject)
