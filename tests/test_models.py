import github3
import requests
from tests.utils import BaseCase, TestCase, RequestsBytesIO, is_py3


class TestGitHubObject(TestCase):
    def test_from_json(self):
        o = github3.models.GitHubObject.from_json({})
        assert isinstance(o, github3.models.GitHubObject)


class TestGitHubCore(BaseCase):
    def setUp(self):
        super(TestGitHubCore, self).setUp()
        self.g = github3.models.GitHubCore({})

    def test_repr(self):
        g = self.g
        assert repr(g) == '<github3-core at 0x{0:x}>'.format(id(g))

    def test_json(self):
        r = requests.Response()
        r.headers['Last-Modified'] = 'foo'
        r.headers['ETag'] = 'bar'
        r.raw = RequestsBytesIO('{}'.encode() if is_py3 else '{}')
        r.status_code = 200

        json = self.g._json(r, 200)
        assert json['Last-Modified'] == 'foo'
        assert json['ETag'] == 'bar'

    def test_boolean(self):
        r = requests.Response()
        r.status_code = 512
        r.raw = RequestsBytesIO('{}'.encode() if is_py3 else '{}')

        self.assertRaises(github3.GitHubError, self.g._boolean, r, 200, 404)


class TestGitHubError(TestCase):
    def __init__(self, methodName='runTest'):
        super(TestGitHubError, self).__init__(methodName)
        self.r = requests.Response()
        self.r.status_code = 400
        message = '{"message": "m", "errors": ["e"]}'
        self.r.raw = RequestsBytesIO(message.encode() if is_py3 else message)
        self.error = github3.models.GitHubError(self.r)

    def test_repr(self):
        assert repr(self.error) == '<GitHubError [m]>'

    def test_str(self):
        assert str(self.error) == '400 m'

    def test_message(self):
        assert self.error.message == self.error.msg

    def test_amazon(self):
        r = requests.Response()
        r.status_code = 400
        r.raw = RequestsBytesIO()
        e = github3.models.GitHubError(r)
        assert e.message == '[No message]'
