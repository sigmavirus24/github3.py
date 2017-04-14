"""Integration tests for methods implemented on Branch."""
from .helper import IntegrationHelper


class TestBranch(IntegrationHelper):
    """Branch integration tests."""

    betamax_kwargs = {'match_requests_on': ['method', 'uri', 'json-body']}

    def test_protection_full(self):
        expected = {
            u'ETag': 'W/"5cb82b3fb62e3186550c207ba2c5cebe"',
            u'Last-Modified': u'',
            u'enforce_admins': {
                u'enabled': True,
                u'url': u'https://api.github.com/repos/discogestalt/github3.py/branches/protected/protection/enforce_admins'
            },
            u'required_pull_request_reviews': {
                u'include_admins': True,
                u'url': u'https://api.github.com/repos/discogestalt/github3.py/branches/protected/protection/required_pull_request_reviews'
            },
            u'required_status_checks': {
                u'contexts': [],
                u'contexts_url': u'https://api.github.com/repos/discogestalt/github3.py/branches/protected/protection/required_status_checks/contexts',
                u'include_admins': True,
                u'strict': True,
                u'url': u'https://api.github.com/repos/discogestalt/github3.py/branches/protected/protection/required_status_checks'
            },
            u'url': u'https://api.github.com/repos/discogestalt/github3.py/branches/protected/protection'
        }

        self.token_login()
        cassette_name = self.cassette_name('protection_full')
        with self.recorder.use_cassette(cassette_name, **self.betamax_kwargs):
            repository = self.gh.repository('discogestalt', 'github3.py')
            branch = repository.branch('protected')
            protection_full = branch.protection_full()
            assert protection_full == expected

    def test_protect(self):
        expected = {
            'enabled': True,
            'required_status_checks': {'enforcement_level': 'off',
                                       'contexts': []}}
        required = expected['required_status_checks']

        self.token_login()
        cassette_name = self.cassette_name('protect')
        with self.recorder.use_cassette(cassette_name, **self.betamax_kwargs):
            repository = self.gh.repository('bboe', 'github3.py')
            branch = repository.branch('develop')

            # Initial change
            branch.protect('off', [])
            assert branch.protection == expected

            # Change status_checks
            branch.protect(None, ['a'])
            required['contexts'] = ['a']
            assert branch.protection == expected

            # Change enforcement
            branch.protect('everyone')
            required['enforcement_level'] = 'everyone'
            assert branch.protection == expected

            # Clear status_checks
            branch.protect(None, [])
            required['contexts'] = []
            assert branch.protection == expected

    def test_unprotect(self):
        expected = {
            'enabled': False,
            'required_status_checks': {'enforcement_level': 'off',
                                       'contexts': []}}

        self.token_login()
        cassette_name = self.cassette_name('unprotect')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('bboe', 'github3.py')
            branch = next(repository.branches(protected=True))
            branch.unprotect()
            assert branch.protection == expected

    def test_latest_sha(self):
        cassette_name = self.cassette_name('latest_sha')
        betamax_kwargs = {
            'match_requests_on': ['method', 'uri', 'if-none-match']
        }
        with self.recorder.use_cassette(cassette_name, **betamax_kwargs):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            branch = repository.branch('develop')
            sha = '872c813ffb7a40c96c3252d764e4838444905ad9'
            latest_sha = branch.latest_sha(differs_from=sha)

        assert latest_sha is None

    def test_latest_sha_differs(self):
        cassette_name = self.cassette_name('latest_sha_differs')
        betamax_kwargs = {
            'match_requests_on': ['method', 'uri', 'if-none-match']
        }
        with self.recorder.use_cassette(cassette_name, **betamax_kwargs):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            branch = repository.branch('develop')
            sha = 'fakesha12'
            latest_sha = branch.latest_sha(differs_from=sha)

        assert latest_sha
