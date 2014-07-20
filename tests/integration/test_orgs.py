# -*- coding: utf-8 -*-
"""Integration tests for methods implemented on Organization."""
import github3

from .helper import IntegrationHelper


class TestOrganization(IntegrationHelper):

    """Organization integration tests."""

    betamax_kwargs = {'match_requests_on': ['method', 'uri', 'json-body']}

    def test_add_member(self):
        """Test the ability to add a member to an organization."""
        self.basic_login()
        cassette_name = self.cassette_name('add_member')
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization('github3py')
            assert isinstance(o, github3.orgs.Organization)
            for team in o.teams():
                if team.name == 'Do Not Delete':
                    break
            else:
                assert False, 'Could not find team'
            assert o.add_member('esacteksab', team.id) is True

    def test_add_repository(self):
        """Test the ability to add a repository to an organization."""
        self.basic_login()
        cassette_name = self.cassette_name('add_repository')
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization('github3py')
            assert isinstance(o, github3.orgs.Organization)

            for team in o.teams():
                if team.name == 'Do Not Delete':
                    break
            else:
                assert False, 'Could not find team'

            assert o.add_repository('github3py/urllib3', team.id) is True

    def test_create_repository(self):
        """Test the ability to create a repository in an organization."""
        self.basic_login()
        cassette_name = self.cassette_name('create_repository')
        with self.recorder.use_cassette(cassette_name, **self.betamax_kwargs):
            o = self.gh.organization('github3py')
            assert isinstance(o, github3.orgs.Organization)

            r = o.create_repository('test-repository', description='hi')
            assert isinstance(r, github3.repos.Repository)
            assert r.delete() is True
