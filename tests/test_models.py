import github3
import requests
from tests.utils import BaseCase, TestCase, expect, BytesIO, is_py3


class TestGitHubObject(TestCase):
    def test_from_json(self):
        o = github3.models.GitHubObject.from_json({})
        expect(o).isinstance(github3.models.GitHubObject)


class TestGitHubCore(BaseCase):
    def setUp(self):
        super(TestGitHubCore, self).setUp()
        self.g = github3.models.GitHubCore({})

    def test_repr(self):
        g = self.g
        expect(repr(g)) == '<github3-core at 0x{0:x}>'.format(id(g))

    def test_json(self):
        r = requests.Response()
        r.headers['Last-Modified'] = 'foo'
        r.headers['ETag'] = 'bar'
        r.raw = BytesIO('{}'.encode() if is_py3 else '{}')
        r.status_code = 200

        json = self.g._json(r, 200)
        expect(json['Last-Modified']) == 'foo'
        expect(json['ETag']) == 'bar'

    def test_boolean(self):
        r = requests.Response()
        r.status_code = 512
        r.raw = BytesIO('{}'.encode() if is_py3 else '{}')

        with expect.githuberror():
            self.g._boolean(r, 200, 404)

    def test_ratelimit_remaining(self):
        self.response('ratelimit')
        self.get(self.github_url + 'rate_limit')

        expect(self.g.ratelimit_remaining) == 60
        self.mock_assertions()


class TestGitHubError(TestCase):
    def __init__(self, methodName='runTest'):
        super(TestGitHubError, self).__init__(methodName)
        self.r = requests.Response()
        self.r.status_code = 400
        message = '{"message": "m", "errors": ["e"]}'
        self.r.raw = BytesIO(message.encode() if is_py3 else message)
        self.error = github3.models.GitHubError(self.r)

    def test_repr(self):
        expect(repr(self.error)) == '<GitHubError [m]>'

    def test_str(self):
        expect(str(self.error)) == '400 m'

    def test_message(self):
        expect(self.error.message) == self.error.msg

    def test_amazon(self):
        r = requests.Response()
        r.status_code = 400
        r.raw = BytesIO()
        e = github3.models.GitHubError(r)
        expect(e.message) == '[No message]'
