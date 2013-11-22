import pytest

from github3 import session


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
            assert s.auth != auth

    def test_basic_login(self):
        """Test that basic auth will work with a valid combination"""
        s = self.build_session()
        s.basic_auth('username', 'password')
        assert s.auth == ('username', 'password')

    def test_token_auth(self):
        """Test that token auth will work with a valid token"""
        s = self.build_session()
        s.token_auth('token goes here')
        assert s.headers['Authorization'] == 'token token goes here'

    def test_token_auth_does_not_use_falsey_values(self):
        """Test that token auth will not authenticate with falsey values"""
        bad_tokens = [None, '']
        for token in bad_tokens:
            s = self.build_session()
            s.token_auth(token)
            assert 'Authorization' not in s.headers

    def test_oauth2_auth(self):
        """Test that oauth2 authentication works

        For now though, it doesn't because it isn't implemented.
        """
        s = self.build_session()
        with pytest.raises(NotImplementedError):
            s.oauth2_auth('Foo', 'bar')
