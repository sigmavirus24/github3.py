import github3
from json import dumps
from mock import MagicMock
from unittest import TestCase
from expecter import expect


class TestGitHub(TestCase):
    def setUp(self):
        self.g_anon = github3.GitHub()
        self.mock_anon = self.g._session = MagicMock(name='anon')
        self.mock_anon.auth = ()
        self.sess_mock = github3.session = MagicMock(name='auth')
        self.mock_auth = self.g_auth = github3.GitHub()
        self.mock_auth.auth = ('user', 'password')

    def test_authorization(self):
        url = 'https://api.github.com/authorizations/10'
        expect(self.g_anon.authorization(10)).raises(github3.GitHubError)
        self.g_auth.authorization(10)
        self.mock_auth.get.assert_called_with(url)

    def test_authorize(self):
        url = 'https://api.github.com/authorizations'
        scopes = ['scope1', 'scope2']
        json_scopes = dumps(scopes)

        def assertions(args):
            assert url in args
            assert json_scopes in args
            assert '"note": ""' in args
            assert '"note_url": ""' in args

        self.g_anon.authorize(None, None, scopes)
        assert self.mock_anon.post.call_count == 0

        self.g_anon.authorize('user', 'password', scopes)
        assertions(self.mock_anon.post.call_args[0])

        self.g.auth = ('user', 'password')
        self.g_anon.authorize(None, None, scopes)
        assert self.sess_mock.post.call_count == 1
        assertions(self.sess_mock.post.call_args[0])
