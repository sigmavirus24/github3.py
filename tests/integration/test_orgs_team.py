# -*- coding: utf-8 -*-
"""Integration tests for methods implemented on Team."""
import github3

from .helper import IntegrationHelper


class TestTeam(IntegrationHelper):

    """Team integration tests."""

    betamax_kwargs = {'match_requests_on': ['method', 'uri', 'json-body']}

    def setUp(self):
        super(TestTeam, self).setUp()
        self.auto_login()

    def get_organization(self, organization='github3py'):
        """Get the desired organization."""
        o = self.gh.organization(organization)
        assert isinstance(o, github3.orgs.Organization)
        return o

    def get_team(self, organization='github3py', id=189901):
        """Get our desired team."""
        o = self.get_organization(organization)
        t = o.team(id)
        assert isinstance(t, github3.orgs.Team)
        return t

    def test_add_member(self):
        """Show a user can add a member to a team."""
        cassette_name = self.cassette_name('add_member')
        with self.recorder.use_cassette(cassette_name):
            team = self.get_team()
            assert team.add_member('esacteksab') is True

    def test_add_repository(self):
        """Show that a user can add a repository to a team."""
        cassette_name = self.cassette_name('add_repository')
        with self.recorder.use_cassette(cassette_name):
            team = self.get_team()
            assert team.add_repository('github3py/urllib3') is True

    def test_delete(self):
        """Show that a user can delete a team."""
        cassette_name = self.cassette_name('delete')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()
            t = o.create_team('delete-me')
            assert isinstance(t, github3.orgs.Team)
            assert t.delete() is True

    def test_edit(self):
        """Show that a user can edit a team."""
        cassette_name = self.cassette_name('edit')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()
            # Create a new team to play with
            t = o.create_team('edit-me')
            assert isinstance(t, github3.orgs.Team)
            # Edit the new team
            assert t.edit('delete-me', permission='admin') is True
            # Assert that the name has changed
            assert t.name == 'delete-me'
            # Get rid of it, we don't need it.
            assert t.delete() is True

    def test_has_repository(self):
        """Show that a user can check of a team has access to a repository."""
        cassette_name = self.cassette_name('has_repository')
        with self.recorder.use_cassette(cassette_name):
            t = self.get_team()
            assert t.has_repository('github3py/urllib3') is True

    def test_is_member(self):
        """Show that a user can check if another user is a team member."""
        cassette_name = self.cassette_name('is_member')
        with self.recorder.use_cassette(cassette_name):
            t = self.get_team()
            assert t.is_member('sigmavirus24') is True

    def test_members(self):
        """Show that a user can retrieve a team's members."""
        cassette_name = self.cassette_name('members')
        with self.recorder.use_cassette(cassette_name):
            t = self.get_team()
            for member in t.members():
                assert isinstance(member, github3.users.ShortUser)

    def test_can_filter_members_by_role(self):
        """Test the ability to filter an team's members by role."""
        self.auto_login()
        cassette_name = self.cassette_name('members_roles')
        with self.recorder.use_cassette(cassette_name):
            t = self.get_team()
            for member in t.members(role='all'):
                assert isinstance(member, github3.users.ShortUser)

    def test_repositories(self):
        """Show that a user can retrieve a team's repositories."""
        cassette_name = self.cassette_name('repositories')
        with self.recorder.use_cassette(cassette_name):
            t = self.get_team()
            for repository in t.repositories():
                assert isinstance(repository, github3.repos.ShortRepository)

    def test_remove_member(self):
        """Show a user can remove a member from a team."""
        cassette_name = self.cassette_name('remove_member')
        with self.recorder.use_cassette(cassette_name):
            team = self.get_team()
            assert team.remove_member('esacteksab') is True

    def test_remove_repository(self):
        """Show a user can remove a repository from a team."""
        cassette_name = self.cassette_name('remove_repository')
        with self.recorder.use_cassette(cassette_name):
            team = self.get_team(id=923595)
            assert team.remove_repository('github3py/urllib3') is True
