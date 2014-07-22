# -*- coding: utf-8 -*-
"""Integration tests for methods implemented on Team."""
import pytest

import github3

from .helper import IntegrationHelper


class TestTeam(IntegrationHelper):

    """Team integration tests."""

    betamax_kwargs = {'match_requests_on': ['method', 'uri', 'json-body']}

    def get_team(self, organization='github3py', id=189901):
        """Get our desired team."""
        o = self.gh.organization(organization)
        assert isinstance(o, github3.orgs.Organization)
        t = o.team(id)
        assert isinstance(t, github3.orgs.Team)
        return t

    def test_add_member(self):
        """Show a user can add a member to a team."""
        self.basic_login()
        cassette_name = self.cassette_name('add_member')
        with self.recorder.use_cassette(cassette_name):
            team = self.get_team()
            assert team.add_member('esacteksab') is True

    def test_remove_member(self):
        """Show a user can remove a member from a team."""
        self.basic_login()
        cassette_name = self.cassette_name('remove_member')
        with self.recorder.use_cassette(cassette_name):
            team = self.get_team()
            assert team.remove_member('esacteksab') is True
