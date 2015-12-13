"""Integration tests for methods implemented on Branch."""
from .helper import IntegrationHelper


class TestBranch(IntegrationHelper):
    """Branch integration tests."""

    betamax_kwargs = {'match_requests_on': ['method', 'uri', 'json-body']}

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
