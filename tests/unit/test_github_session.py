try:
    import cPickle as pickle
except ImportError:
    import pickle

import pytest

import requests

from github3 import session
from .helper import mock


class TestGitHubSession:
    def build_session(self, base_url=None):
        s = session.GitHubSession()
        if base_url:
            s.base_url = base_url
        return s

    def test_has_default_headers(self):
        """Assert the default headers are there upon initialization"""
        s = self.build_session()
        assert 'Accept' in s.headers
        assert s.headers['Accept'] == 'application/vnd.github.v3.full+json'
        assert 'Accept-Charset' in s.headers
        assert s.headers['Accept-Charset'] == 'utf-8'
        assert 'Content-Type' in s.headers
        assert s.headers['Content-Type'] == 'application/json'
        assert 'User-Agent' in s.headers
        assert s.headers['User-Agent'].startswith('github3.py/')

    def test_build_url(self):
        """Test that GitHubSessions build basic URLs"""
        s = self.build_session()
        url = s.build_url('gists', '123456', 'history')
        assert url == 'https://api.github.com/gists/123456/history'

    def test_build_url_caches_built_urls(self):
        """Test that building a URL caches it"""
        s = self.build_session()
        url = s.build_url('gists', '123456', 'history')
        url_parts = ('https://api.github.com', 'gists', '123456', 'history')
        assert url_parts in session.__url_cache__
        assert url in session.__url_cache__.values()

    def test_build_url_uses_a_different_base(self):
        """Test that you can pass in a different base URL to build_url"""
        s = self.build_session()
        url = s.build_url('gists', '123456', 'history',
                          base_url='https://status.github.com')
        assert url == 'https://status.github.com/gists/123456/history'

    def test_build_url_respects_the_session_base_url(self):
        """Test that build_url uses the session's base_url"""
        s = self.build_session('https://enterprise.customer.com')
        url = s.build_url('gists')
        assert url == 'https://enterprise.customer.com/gists'

    def test_basic_login_does_not_use_falsey_values(self):
        """Test that basic auth will not authenticate with falsey values"""
        bad_auths = [
            (None, 'password'),
            ('username', None),
            ('', 'password'),
            ('username', ''),
            ]
        for auth in bad_auths:
            # Make sure we have a clean session to test with
            s = self.build_session()
            s.basic_auth(*auth)
            assert s.auth != session.BasicAuth(*auth)

    def test_basic_login(self):
        """Test that basic auth will work with a valid combination"""
        s = self.build_session()
        s.basic_auth('username', 'password')
        assert s.auth == session.BasicAuth('username', 'password')

    def test_basic_login_disables_token_auth(self):
        """Test that basic auth will remove the Authorization header.

        Token and basic authentication will conflict so remove the token
        authentication.
        """
        s = self.build_session()
        s.token_auth('token goes here')
        req = requests.Request('GET', 'https://api.github.com/')
        pr = s.prepare_request(req)
        assert 'token token goes here' == pr.headers['Authorization']
        s.basic_auth('username', 'password')
        pr = s.prepare_request(req)
        assert 'token token goes here' != pr.headers['Authorization']

    @mock.patch.object(requests.Session, 'request')
    def test_handle_two_factor_auth(self, request_mock):
        """Test the method that handles getting the 2fa code"""
        s = self.build_session()
        s.two_factor_auth_callback(lambda: 'fake')
        args = ('GET', 'http://example.com')
        s.handle_two_factor_auth(args, {})
        request_mock.assert_called_once_with(
            *args,
            headers={'X-GitHub-OTP': 'fake'}
            )

    @mock.patch.object(requests.Session, 'request')
    def test_request_ignores_responses_that_do_not_require_2fa(self,
                                                               request_mock):
        """Test that request does not try to handle 2fa when it should not"""
        response = mock.Mock()
        response.configure_mock(status_code=200, headers={})
        request_mock.return_value = response
        s = self.build_session()
        s.two_factor_auth_callback(lambda: 'fake')
        r = s.get('http://example.com')
        assert r is response
        request_mock.assert_called_once_with(
            'GET', 'http://example.com', allow_redirects=True
            )

    @mock.patch.object(requests.Session, 'request')
    def test_creates_history_while_handling_2fa(self, request_mock):
        """Test that the overridden request method will create history"""
        response = mock.Mock()
        response.configure_mock(
            status_code=401,
            headers={'X-GitHub-OTP': 'required;2fa'},
            history=[]
            )
        request_mock.return_value = response
        s = self.build_session()
        s.two_factor_auth_callback(lambda: 'fake')
        r = s.get('http://example.com')
        assert len(r.history) != 0
        assert request_mock.call_count == 2

    def test_token_auth(self):
        """Test that token auth will work with a valid token"""
        s = self.build_session()
        s.token_auth('token goes here')
        req = requests.Request('GET', 'https://api.github.com/')
        pr = s.prepare_request(req)
        assert pr.headers['Authorization'] == 'token token goes here'

    def test_token_auth_disables_basic_auth(self):
        """Test that using token auth removes the value of the auth attribute.

        If `GitHubSession.auth` is set then it conflicts with the token value.
        """
        s = self.build_session()
        s.auth = ('foo', 'bar')
        s.token_auth('token goes here')
        assert s.auth != ('foo', 'bar')
        assert isinstance(s.auth, session.TokenAuth)

    def test_token_auth_does_not_use_falsey_values(self):
        """Test that token auth will not authenticate with falsey values"""
        bad_tokens = [None, '']
        req = requests.Request('GET', 'https://api.github.com/')
        for token in bad_tokens:
            s = self.build_session()
            s.token_auth(token)
            pr = s.prepare_request(req)
            assert 'Authorization' not in pr.headers

    def test_token_auth_with_netrc_works(self, tmpdir):
        """
        Test that token auth will be used instead of netrc.

        With no auth specified, requests will use any matching auths
        in .netrc/_netrc files
        """
        token = "my-valid-token"
        s = self.build_session()
        s.token_auth(token)

        netrc_contents = (
            "machine api.github.com\n"
            "login sigmavirus24\n"
            "password invalid_token_for_test_verification\n"
        )
        # cover testing netrc behaviour on different OSs
        dotnetrc = tmpdir.join(".netrc")
        dotnetrc.write(netrc_contents)
        dashnetrc = tmpdir.join("_netrc")
        dashnetrc.write(netrc_contents)

        with mock.patch.dict('os.environ', {'HOME': str(tmpdir)}):
            # prepare_request triggers reading of .netrc files
            pr = s.prepare_request(
                requests.Request(
                    'GET', 'https://api.github.com/users/sigmavirus24')
            )
            auth_header = pr.headers['Authorization']
            assert auth_header == 'token {0}'.format(token)

    def test_two_factor_auth_callback_handles_None(self):
        s = self.build_session()
        assert s.two_factor_auth_cb is None
        s.two_factor_auth_callback(None)
        assert s.two_factor_auth_cb is None

    def test_two_factor_auth_callback_checks_for_Callable(self):
        s = self.build_session()
        assert s.two_factor_auth_cb is None
        with pytest.raises(ValueError):
            s.two_factor_auth_callback(1)

    def test_two_factor_auth_callback_accepts_a_Callable(self):
        s = self.build_session()
        assert s.two_factor_auth_cb is None
        # You have to have a sense of humor ;)

        def _not_so_anonymous(*args):
            return 'foo'

        not_so_anonymous = _not_so_anonymous
        s.two_factor_auth_callback(not_so_anonymous)
        assert s.two_factor_auth_cb is not_so_anonymous

    def test_oauth2_auth(self):
        """Test that oauth2 authentication works

        For now though, it doesn't because it isn't implemented.
        """
        s = self.build_session()
        with pytest.raises(NotImplementedError):
            s.oauth2_auth('Foo', 'bar')

    def test_issubclass_of_requests_Session(self):
        """Test that GitHubSession is a subclass of requests.Session"""
        assert issubclass(session.GitHubSession,
                          requests.Session)

    def test_can_use_temporary_basic_auth(self):
        """Test that temporary_basic_auth resets old auth."""
        s = self.build_session()
        s.basic_auth('foo', 'bar')
        with s.temporary_basic_auth('temp', 'pass'):
            assert s.auth != session.BasicAuth('foo', 'bar')

        assert s.auth == session.BasicAuth('foo', 'bar')

    def test_temporary_basic_auth_replaces_auth(self):
        """Test that temporary_basic_auth sets the proper credentials."""
        s = self.build_session()
        s.basic_auth('foo', 'bar')
        with s.temporary_basic_auth('temp', 'pass'):
            assert s.auth == session.BasicAuth('temp', 'pass')

    def test_no_auth(self):
        """Verify that no_auth removes existing authentication."""
        s = self.build_session()
        s.basic_auth('user', 'password')
        req = requests.Request('GET', 'https://api.github.com/')

        with s.no_auth():
            pr = s.prepare_request(req)
            assert 'Authorization' not in pr.headers
            assert s.auth is None

        pr = s.prepare_request(req)
        assert 'Authorization' in pr.headers
        assert s.auth == session.BasicAuth('user', 'password')

    def test_retrieve_client_credentials_when_set(self):
        """Test that retrieve_client_credentials will return the credentials.

        We must assert that when set, this function will return them.
        """
        s = self.build_session()
        s.params = {'client_id': 'id', 'client_secret': 'secret'}
        assert s.retrieve_client_credentials() == ('id', 'secret')

    def test_retrieve_client_credentials_returns_none(self):
        """Test that retrieve_client_credentials will return (None, None).

        Namely, then the necessary parameters are set, it will not raise an
        error.
        """
        s = self.build_session()
        assert s.retrieve_client_credentials() == (None, None)

    def test_pickling(self):
        s = self.build_session('https://api.github.com')
        dumped = pickle.dumps(s, pickle.HIGHEST_PROTOCOL)
        loaded = pickle.loads(dumped)

        assert hasattr(loaded, 'base_url')
        assert hasattr(loaded, 'two_factor_auth_cb')

        assert loaded.base_url == s.base_url
        assert loaded.two_factor_auth_cb == s.two_factor_auth_cb
