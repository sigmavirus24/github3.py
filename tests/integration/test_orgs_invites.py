# -*- coding: utf-8 -*-
"""Integration tests for invitation methods implemented on orgs."""
import github3

from .helper import IntegrationHelper


class TestInvitations(IntegrationHelper):

    """Team integration tests."""

    betamax_kwargs = {'match_requests_on': ['method', 'uri', 'json-body']}

    def setUp(self):
        super(TestInvitations, self).setUp()
        self.basic_login()

    def get_organization(self, name='mozillatw'):
        """Get the organization for each test."""
        self.token_login()
        o = self.gh.organization(name)
        assert isinstance(o, github3.orgs.Organization)
        return o

    def test_invites(self):
        """Show that a user can retrieve an org's invites."""
        cassette_name = self.cassette_name('invitations')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()
            for invite in o.invitations():
                assert isinstance(invite, dict)
