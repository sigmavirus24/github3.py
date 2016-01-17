import github3

from .helper import IntegrationHelper


class TestGitHubSession(IntegrationHelper):
    def test_two_factor_authentication_works(self):
        def _two_factor_auth():
            return '862478'
        two_factor_auth = _two_factor_auth
        self.basic_login()
        self.gh.login(two_factor_callback=two_factor_auth)

        cassette_name = self.cassette_name('two_factor_authentication')
        assert isinstance(self.session, github3.session.GitHubSession)

        match = ['method', 'uri', 'gh3-headers']
        with self.recorder.use_cassette(cassette_name,
                                        match_requests_on=match):
            r = self.session.get('https://api.github.com/users/sigmavirus24')
            assert r.status_code == 200
