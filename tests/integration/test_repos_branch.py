"""Integration tests for methods implemented on Branch."""
from .helper import IntegrationHelper


class TestBranch(IntegrationHelper):
    """Branch integration tests."""

    betamax_kwargs = {'match_requests_on': ['method', 'uri', 'json-body']}

    def test_protection_full(self):
        self.token_login()
        cassette_name = self.cassette_name('protection_full')
        with self.recorder.use_cassette(cassette_name, **self.betamax_kwargs):
            repository = self.gh.repository('discogestalt', 'github3.py')
            branch = repository.branch('protected')
            pf = branch.protection_full()
            assert pf['enforce_admins']['enabled']
            assert pf['required_pull_request_reviews']['include_admins']
            assert pf['required_status_checks']['include_admins']
            assert pf['required_status_checks']['strict']

    def test_protect(self):
        expected = {
            'enabled': True,
            'required_status_checks': {'enforcement_level': 'off',
                                       'contexts': []}}
        required = expected['required_status_checks']

        self.token_login()
        cassette_name = self.cassette_name('protect')
        with self.recorder.use_cassette(cassette_name, **self.betamax_kwargs):
            repository = self.gh.repository('github3py', 'github3.py')
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
            repository = self.gh.repository('github3py', 'github3.py')
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
            sha = 'b58ff53ce9607f71aeb06f46eefe991f83c5e83e'
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
