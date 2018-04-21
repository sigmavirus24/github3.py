"""Integration tests for methods implemented on Branch."""
import pytest

from .helper import IntegrationHelper


class TestBranch(IntegrationHelper):
    """Branch integration tests."""

    betamax_kwargs = {'match_requests_on': ['method', 'uri', 'json-body']}

    @pytest.mark.xfail
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
            assert branch.original_protection is None

            # Change status_checks
            branch.protect(None, ['a'])
            required['contexts'] = ['a']
            assert branch.original_protection == expected

            # Change enforcement
            branch.protect('everyone')
            required['enforcement_level'] = 'everyone'
            assert branch.original_protection == expected

            # Clear status_checks
            branch.protect(None, [])
            required['contexts'] = []
            assert branch.original_protection == expected

    @pytest.mark.xfail
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
            assert branch.original_protection == expected

    def test_latest_sha(self):
        cassette_name = self.cassette_name('latest_sha')
        betamax_kwargs = {
            'match_requests_on': ['method', 'uri', 'if-none-match']
        }
        with self.recorder.use_cassette(cassette_name, **betamax_kwargs):
            repository = self.gh.repository('PyCQA', 'flake8')
            branch = repository.branch('stable/2.6')
            sha = '1254fe8f5cfcbd4afc2f692827da4f04a3033c56'
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
            sha = '541468cdfde6cffe55f0cc801186cdffed154a6a'
            latest_sha = branch.latest_sha(differs_from=sha)

        assert not isinstance(latest_sha, bytes)
