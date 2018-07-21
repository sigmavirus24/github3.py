# -*- coding: utf-8 -*-
"""Integration tests for methods implemented on Organization."""
import pytest

import github3

from .helper import IntegrationHelper


class TestOrganization(IntegrationHelper):

    """Organization integration tests."""

    betamax_kwargs = {'match_requests_on': ['method', 'uri', 'json-body']}

    def get_organization(self, name='github3py', auth_needed=False):
        """Get the organization for each test."""
        if auth_needed:
            self.token_login()
        o = self.gh.organization(name)
        assert isinstance(o, github3.orgs.Organization)
        return o

    def get_team(self, organization, team_name='Do Not Delete'):
        """Get the desired team."""
        for team in organization.teams():
            if team.name == team_name:
                break
        else:
            assert False, 'Could not find team "{0}"'.format(team_name)

        return team

    def test_add_member(self):
        """Test the ability to add a member to an organization."""
        self.auto_login()
        cassette_name = self.cassette_name('add_member')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()
            team = self.get_team(o)
            assert o.add_member('esacteksab', team.id) is True

    def test_add_repository(self):
        """Test the ability to add a repository to an organization."""
        self.auto_login()
        cassette_name = self.cassette_name('add_repository')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()
            team = self.get_team(o)
            assert o.add_repository('github3py/urllib3', team.id) is True

    def test_create_project(self):
        """Test the ability to create a project in an organization."""
        self.token_login()
        cassette_name = self.cassette_name('create_org_project')
        with self.recorder.use_cassette(cassette_name, **self.betamax_kwargs):
            o = self.get_organization(name='github3py')
            r = o.create_project('test-project', body='test body')
            assert isinstance(r, github3.projects.Project)
            assert r.delete() is True

    def test_create_repository(self):
        """Test the ability to create a repository in an organization."""
        self.auto_login()
        cassette_name = self.cassette_name('create_repository')
        with self.recorder.use_cassette(cassette_name, **self.betamax_kwargs):
            o = self.get_organization()
            r = o.create_repository('test-repository', description='hi')
            assert isinstance(r, github3.repos.Repository)
            assert r.delete() is True

    def test_conceal_member(self):
        """Test the ability to conceal a User's membership."""
        self.auto_login()
        cassette_name = self.cassette_name('conceal_member')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            # Get a public member of the organization
            public_member = next(o.public_members())
            assert isinstance(public_member, github3.users.ShortUser)

            # Conceal their membership
            assert o.conceal_member(public_member) is True
            # Re-publicize their membership
            assert o.publicize_member(public_member) is True

    def test_create_team(self):
        """Test the ability to create a new team."""
        self.auto_login()
        cassette_name = self.cassette_name('create_team')
        with self.recorder.use_cassette(cassette_name, **self.betamax_kwargs):
            o = self.get_organization()

            t = o.create_team('temp-team')
            assert isinstance(t, github3.orgs.Team)
            assert t.delete() is True

    def test_edit(self):
        """Test the ability to edit an organization."""
        self.auto_login()
        cassette_name = self.cassette_name('edit')
        with self.recorder.use_cassette(cassette_name, **self.betamax_kwargs):
            o = self.get_organization()

            assert o.edit(location='Madison, WI') is True
            assert o.edit(description='How people build software.') is True
            assert o.edit(has_organization_projects=False) is True
            assert o.edit(has_repository_projects=False) is True
            assert o.edit(default_repository_permission='write') is True
            assert o.edit(members_can_create_repositories=False) is True

    def test_is_member(self):
        """Test the ability to check if a User is a member of the org."""
        cassette_name = self.cassette_name('is_member')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            assert o.is_member('sigmavirus24') is True

    def test_is_public_member(self):
        """Test the ability to check if a User is a public member."""
        cassette_name = self.cassette_name('is_public_member')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            assert o.is_public_member('defunkt') is False

    def test_all_events(self):
        """Test retrieving organization's complete event stream."""
        self.basic_login()
        cassette_name = self.cassette_name('all_events')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization('testgh3py')

            for event in o.all_events(username='gh3test'):
                assert isinstance(event, github3.events.Event)

    def test_events(self):
        """Test retrieving an organization's public event stream."""
        cassette_name = self.cassette_name('public_events')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            for event in o.events():
                assert isinstance(event, github3.events.Event)
                assert isinstance(event.as_json(), str)

    def test_public_events(self):
        """Test retrieving an organization's public event stream."""
        cassette_name = self.cassette_name('public_events')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            for event in o.public_events():
                assert isinstance(event, github3.events.Event)

    def test_members(self):
        """Test the ability to retrieve an organization's members."""
        self.auto_login()
        cassette_name = self.cassette_name('members')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            for member in o.members():
                assert isinstance(member, github3.users.ShortUser)

    @pytest.mark.xfail(
        reason="sigmavirus24 needs to actually write a test for this."
    )
    def test_can_filter_organization_members(self):
        """
        Test the ability to filter an organization's members by
        their ``"2fa_disabled"`` status. This filter is only
        available to organization owners.
        """
        self.basic_login()
        cassette_name = self.cassette_name('members_filters')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            for member in o.members(filter='2fa_disabled'):
                assert isinstance(member, github3.users.ShortUser)

    def test_can_filter_members_by_role(self):
        """Test the ability to filter an organization's members by role."""
        self.auto_login()
        cassette_name = self.cassette_name('members_roles')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            for member in o.members(role='all'):
                assert isinstance(member, github3.users.ShortUser)

    def test_project(self):
        """Test the ability to retrieve a single organization project."""
        self.token_login()
        cassette_name = self.cassette_name('project')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            # Grab a project, any project
            first_project = next(o.projects())

            fetched_project = o.project(first_project.id)
            assert first_project == fetched_project

    def test_projects(self):
        """Test the ability to retrieve an organization's projects."""
        self.token_login()
        cassette_name = self.cassette_name('projects')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            for project in o.projects():
                assert isinstance(project, github3.projects.Project)

    def test_public_members(self):
        """Test the ability to retrieve an organization's public members."""
        self.auto_login()
        cassette_name = self.cassette_name('public_members')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            for member in o.public_members():
                assert isinstance(member, github3.users.ShortUser)

    def test_repositories(self):
        """Test the ability to retrieve an organization's repositories."""
        cassette_name = self.cassette_name('repositories')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            for repo in o.repositories():
                assert isinstance(repo, github3.repos.ShortRepository)

    def test_teams(self):
        """Test the ability to retrieve an organization's teams."""
        self.auto_login()
        cassette_name = self.cassette_name('teams')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            for team in o.teams():
                assert isinstance(team, github3.orgs.ShortTeam)

    def test_publicize_member(self):
        """Test the ability to publicize a member of the organization."""
        self.auto_login()
        cassette_name = self.cassette_name('publicize_member')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            # Show that we cannot publicize someone other than the current
            # user
            with pytest.raises(github3.GitHubError):
                o.publicize_member('esacteksab')

            assert o.publicize_member('omgjlk') is True

    def test_remove_member(self):
        """Test the ability to remove a member of the organization."""
        self.auto_login()
        cassette_name = self.cassette_name('remove_member')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()
            team = self.get_team(o)

            # First add the user
            assert o.add_member('gh3test', team.id) is True
            # Now remove them
            assert o.remove_member('gh3test') is True

    def test_remove_repository(self):
        """Test the ability to remove a repository from a team."""
        self.auto_login()
        cassette_name = self.cassette_name('remove_repository')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()
            team = self.get_team(o)
            assert o.remove_repository('github3py/urllib3', team.id) is True

    def test_team(self):
        """Test the ability retrieve an individual team by id."""
        self.auto_login()
        cassette_name = self.cassette_name('team')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization()

            # Grab a team, any team
            first_team = next(o.teams())

            fetched_team = o.team(first_team.id)
            assert first_team == fetched_team

    def test_invitations(self):
        """Show that a user can retrieve an org's invites."""
        cassette_name = self.cassette_name('invitations')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization('mozillatw', auth_needed=True)
            for invite in o.invitations():
                assert isinstance(invite, github3.orgs.Invitation)

    def test_invite(self):
        """Show that a user can invite a new member."""
        cassette_name = self.cassette_name('invite')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization(auth_needed=True)
            team = self.get_team(o)
            # 2354350 is gh3test
            assert o.invite([team.id], invitee_id=2354350,
                            role='direct_member')

    def test_membership(self):
        """Show that a user can obtain the membership status."""
        cassette_name = self.cassette_name('membership')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization('Thunderbird-client', auth_needed=True)
            assert o.membership_for('AFineOldWine')

    def test_remove_membership(self):
        """Show that a user can remove a member or invite."""
        cassette_name = self.cassette_name('remove_membership')
        with self.recorder.use_cassette(cassette_name):
            o = self.get_organization('Thunderbird-client', auth_needed=True)
            assert o.remove_membership('AFineOldWine')
