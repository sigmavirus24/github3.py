import github3
import requests
from json import dumps
from mock import patch
from unittest import TestCase
from expecter import expect
from utils import generate_response, path


class TestGitHub(TestCase):
    def setUp(self):
        self.get_r = generate_response(open(path('authorization')))
        self.post_r = generate_response(open(path('authorization')), 201)
        self.g_anon = github3.GitHub()

    @patch.object(requests.sessions.Session, 'request')
    def test_authorization(self, request_mock):
        request_mock.return_value = self.get_r
        #url = 'https://api.github.com/authorizations/10'
        with expect.raises(github3.GitHubError):
            self.g_anon.authorization(10)

        self.g_anon.login('user', 'password')
        a = self.g_anon.authorization(10)
        assert isinstance(a, github3.auths.Authorization)
        #self.g_auth.authorization(10)
        #self.mock_auth.get.assert_called_with(url)

    @patch.object(requests.sessions.Session, 'request')
    def test_authorize(self, request_mock):
        request_mock.return_value = self.post_r
        url = 'https://api.github.com/authorizations'
        scopes = ['scope1', 'scope2']
        json_scopes = dumps(scopes)

        def assertions(args):
            assert url in args
            assert json_scopes in args[1]
            assert '"note": ""' in args[1]
            assert '"note_url": ""' in args[1]

        self.g_anon.authorize(None, None, scopes)
        #assert self.mock_anon.post.call_count == 0

        a = self.g_anon.authorize('user', 'password', scopes)
        #calls = self.sess_mock.mock_calls
        #expect(len(calls)) == 4
        assert isinstance(a, github3.auths.Authorization)

        #self.g_auth.authorize(None, None, scopes)
        #assert self.mock_auth.post.call_count == 1
        #assertions(self.mock_auth.post.call_args[0])
