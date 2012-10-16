import github3
from json import dumps
from mock import MagicMock
from unittest import TestCase
from expecter import expect


class TestGitHub(TestCase):
    def setUp(self):
        self.g_anon = github3.GitHub()
        self.mock_anon = self.g_anon._session = MagicMock(name='anon')
        self.mock_anon.auth = ()
        self.sess_mock = github3.github.session = MagicMock(name='session')
        self.g_auth = github3.GitHub()
        self.mock_auth = self.g_auth._session = MagicMock(name='auth')
        self.mock_auth.auth = ('user', 'password')

    def test_authorization(self):
        url = 'https://api.github.com/authorizations/10'
        with expect.raises(github3.GitHubError):
            self.g_anon.authorization(10)

        self.g_auth.authorization(10)
        self.mock_auth.get.assert_called_with(url)

    def test_authorize(self):
        url = 'https://api.github.com/authorizations'
        scopes = ['scope1', 'scope2']
        json_scopes = dumps(scopes)

        def assertions(args):
            assert url in args
            assert json_scopes in args[1]
            assert '"note": ""' in args[1]
            assert '"note_url": ""' in args[1]

        self.g_anon.authorize(None, None, scopes)
        assert self.mock_anon.post.call_count == 0

        self.g_anon.authorize('user', 'password', scopes)
        calls = self.sess_mock.mock_calls
        expect(len(calls)) == 4

        self.g_auth.authorize(None, None, scopes)
        assert self.mock_auth.post.call_count == 1
        assertions(self.mock_auth.post.call_args[0])
