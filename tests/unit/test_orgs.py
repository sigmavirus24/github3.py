"""Organization unit tests."""
import mock
import pytest

from github3 import GitHubError
from github3.orgs import Organization
from github3.projects import Project

from . import helper

url_for = helper.create_url_helper('https://api.github.com/orgs/github')

get_org_example_data = helper.create_example_data_helper('org_example')

example_data = get_org_example_data()


class TestOrganization(helper.UnitHelper):
    """Class-based unit tests for organizations."""

    described_class = Organization
    example_data = get_org_example_data()

    def test_add_member(self):
        """Show that an authenticated user can add a member to an org."""
        self.instance.add_member('user', 10)

        self.session.put.assert_called_once_with(
            'https://api.github.com/teams/10/members/user'
        )

    def test_add_repository(self):
        """Show that one can add a repository to an organization."""
        self.instance.add_repository('name-of-repo', 10)

        self.session.put.assert_called_once_with(
            'https://api.github.com/teams/10/repos/name-of-repo'
        )

    def test_conceal_member(self):
        """Show that one can conceal an organization member."""
        self.instance.conceal_member('concealed')

        self.session.delete.assert_called_once_with(
            url_for('public_members/concealed')
        )

    def test_create_project(self):
        """Show that one can create a project in an organization."""
        self.instance.create_project('test-project', body='project body')

        self.post_called_with(
            url_for('projects'),
            data={
                'name': 'test-project',
                'body': 'project body'
            },
            headers=Project.CUSTOM_HEADERS
        )

    def test_create_repository(self):
        """Show that one can create a repository in an organization."""
        self.instance.create_repository('repo-name', 'description', team_id=1)

        self.post_called_with(
            url_for('repos'),
            data={
                'name': 'repo-name',
                'description': 'description',
                'homepage': '',
                'private': False,
                'has_issues': True,
                'has_wiki': True,
                'auto_init': False,
                'team_id': 1,
                'gitignore_template': '',
                'license_template': ''
            }
        )

    def test_create_team(self):
        """Show that one can create a team in an organization."""
        self.instance.create_team('team-name', permission='push')

        self.post_called_with(
            url_for('teams'),
            data={
                'name': 'team-name',
                'repo_names': [],
                'permission': 'push'
            }
        )

    def test_edit(self):
        """Show that one can edit the organization."""
        email = 'billing@cordas.co'
        corp = 'Company, LLC'
        self.instance.edit(email, company=corp)

        self.patch_called_with(
            url_for(),
            data={
                'billing_email': email,
                'company': corp
            }
        )

    def test_equality(self):
        """Show that a user can compare teams."""
        team = self.create_instance_of_described_class()
        assert team == self.instance

    def test_is_member(self):
        """Show that a user can if another user is an organization member."""
        self.instance.is_member('username')

        self.session.get.assert_called_once_with(url_for('members/username'))

    def test_is_public_member(self):
        """Show that a user can if another user is a public org member."""
        self.instance.is_public_member('username')

        self.session.get.assert_called_once_with(
            url_for('public_members/username')
        )

    def test_project(self):
        """Show that a user can access a single organization project."""
        self.instance.project(400435)

        self.session.get.assert_called_once_with(
            'https://api.github.com/projects/400435',
            headers=Project.CUSTOM_HEADERS
        )

    def test_publicize_member(self):
        """Show that a user can publicize their own membership."""
        self.instance.publicize_member('username')

        self.session.put.assert_called_once_with(
            url_for('public_members/username')
        )

    def test_remove_member(self):
        """Show that one can remove a user from an organization."""
        self.instance.remove_member('username')

        self.session.delete.assert_called_once_with(
            url_for('members/username')
        )

    def test_remove_repository(self):
        """Show that one can remove a repository from a team."""
        self.instance.remove_repository('repo-name', 10)

        self.session.delete.assert_called_once_with(
            'https://api.github.com/teams/10/repos/repo-name'
        )

    def test_repr(self):
        """Assert the Organization name is in the repr."""
        assert 'github' in repr(self.instance)

    def test_remove_repository_requires_positive_team_id(self):
        """Show that remove_repository requires a team_id greater than 0."""
        assert self.instance.remove_repository('name', -1) is False

        assert self.session.delete.called is False

    def test_team(self):
        """Show that a user can retrieve a team by id."""
        self.instance.team(10)

        self.session.get.assert_called_once_with(
            'https://api.github.com/teams/10'
        )

    def test_team_requires_positive_team_id(self):
        """Show that team requires a team_id greater than 0."""
        self.instance.team(-1)

        assert self.session.get.called is False

    def test_invite(self):
        """Show that a user can be invited to an org."""
        self.instance.invite([1, 2, 3], invitee_id=1)
        headers = {'Accept': 'application/vnd.github.dazzler-preview.json'}

        self.post_called_with(
            'https://api.github.com/orgs/github/invitations',
            data={
                'team_ids': [1, 2, 3],
                'invitee_id': 1,
                'role': 'direct_member',
            },
            headers=headers,
        )

    def test_invite_requires_valid_role(self):
        """Validate our validation of roles."""
        with pytest.raises(ValueError):
            self.instance.invite([1, 2], email='user', role='Freddy')

    def test_invite_passes_optional_role(self):
        """Exercise alternative parameters to create an invitation."""
        self.instance.invite([1, 2], email='user', role='admin')
        headers = {'Accept': 'application/vnd.github.dazzler-preview.json'}

        self.post_called_with(
            'https://api.github.com/orgs/github/invitations',
            data={
                'role': 'admin',
                'email': 'user',
                'team_ids': [1, 2],
            },
            headers=headers,
        )

    def test_membership_for(self):
        """Show that a user's invitation status can be queried."""
        self.instance.membership_for('user')

        self.session.get.assert_called_once_with(
            'https://api.github.com/orgs/github/memberships/user'
        )

    def test_remove_membership(self):
        """Show that one can cancel a membership in an organization."""
        self.instance.remove_membership('username')

        self.session.delete.assert_called_once_with(
            url_for('memberships/username')
        )


class TestOrganizationRequiresAuth(helper.UnitRequiresAuthenticationHelper):
    """Unit tests that ensure certain methods require authentication."""

    described_class = Organization
    example_data = get_org_example_data()

    def test_add_member(self):
        """Show that one must be authenticated to add a member to an org."""
        with pytest.raises(GitHubError):
            self.instance.add_member('user', 10)

    def test_add_repository(self):
        """Show that one must be authenticated to add a repo to an org."""
        with pytest.raises(GitHubError):
            self.instance.add_repository('foo', 10)

    def test_conceal_member(self):
        """Show that one must be authenticated to conceal a member."""
        with pytest.raises(GitHubError):
            self.instance.conceal_member('user')

    def test_create_project(self):
        """Show that one must be authenticated to create a project."""
        with pytest.raises(GitHubError):
            self.instance.create_project('name', 'body')

    def test_create_repository(self):
        """Show that one must be authenticated to create a repo for an org."""
        with pytest.raises(GitHubError):
            self.instance.create_repository('foo')

    def test_create_team(self):
        """Show that one must be authenticated to create a team for an org."""
        with pytest.raises(GitHubError):
            self.instance.create_team('foo')

    def test_edit(self):
        """Show that a user must be authenticated to edit an organization."""
        with pytest.raises(GitHubError):
            self.instance.edit('foo')

    def test_publicize_member(self):
        """Show that a user must be authenticated to publicize membership."""
        with pytest.raises(GitHubError):
            self.instance.publicize_member('foo')

    def test_remove_member(self):
        """Show that a user must be authenticated to remove a member."""
        with pytest.raises(GitHubError):
            self.instance.remove_member('foo')

    def test_remove_repository(self):
        """Show that a user must be authenticated to remove a repository."""
        with pytest.raises(GitHubError):
            self.instance.remove_repository('repo-name', 10)

    def test_team(self):
        """Show that a user must be authenticated to retrieve a team."""
        with pytest.raises(GitHubError):
            self.instance.team(10)

    def test_invitations(self):
        """Verify retrieving invitations requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.invitations()

    def test_invite(self):
        """Show that inviting a member requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.invite()

    def test_membership_for(self):
        """Show that inviting a member requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.membership_for()

    def test_remove_membership(self):
        """Show that inviting a member requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.remove_membership()


class TestOrganizationIterator(helper.UnitIteratorHelper):
    """Test Organization methods that return iterators."""

    described_class = Organization
    example_data = example_data.copy()

    def test_all_events(self):
        """Verify the request made from all_events."""
        i = self.instance.all_events(username='dummy')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            'https://api.github.com/users/dummy/events/orgs/github',
            params={'per_page': 100},
            headers={}
        )

    @mock.patch('warnings.warn')
    def test_events(self, warn_mock):
        """Show that one can iterate over an organization's events."""
        i = self.instance.events()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('events'),
            params={'per_page': 100},
            headers={}
        )

        warn_mock.assert_called_once_with(
            'This method is deprecated. Please use ``public_events`` instead.',
            DeprecationWarning)

    def test_members(self):
        """Show that one can iterate over all members."""
        i = self.instance.members()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('members'),
            params={'per_page': 100},
            headers={}
        )

    def test_members_filters(self):
        """Show that one can iterate over all members with 2fa_disabled."""
        i = self.instance.members(filter='2fa_disabled')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('members'),
            params={'per_page': 100, 'filter': '2fa_disabled'},
            headers={}
        )

    def test_members_excludes_fake_filters(self):
        """Show that one cannot pass a bogus filter to the API."""
        i = self.instance.members(filter='bogus-filter')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('members'),
            params={'per_page': 100},
            headers={}
        )

    def test_members_roles(self):
        """Show that one can iterate over all admins."""
        i = self.instance.members(role='admin')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('members'),
            params={'per_page': 100, 'role': 'admin'},
            headers={'Accept': 'application/vnd.github.ironman-preview+json'}
        )

    def test_members_excludes_fake_roles(self):
        """Show that one cannot pass a bogus role to the API."""
        i = self.instance.members(role='bogus-role')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('members'),
            params={'per_page': 100},
            headers={}
        )

    def test_projects(self):
        """Show that a user can access all organization projects."""
        i = self.instance.projects()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('projects'),
            params={'per_page': 100},
            headers=Project.CUSTOM_HEADERS
        )

    def test_public_events(self):
        """Show that one can iterate over an organization's public events."""
        i = self.instance.public_events()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('events'),
            params={'per_page': 100},
            headers={}
        )

    def test_public_members(self):
        """Show that one can iterate over all public members."""
        i = self.instance.public_members()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('public_members'),
            params={'per_page': 100},
            headers={}
        )

    def test_repositories(self):
        """Show that one can iterate over an organization's repositories."""
        i = self.instance.repositories()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('repos'),
            params={'per_page': 100},
            headers={}
        )

    def test_respositories_accepts_type(self):
        """Show that one can pass a repository type."""
        i = self.instance.repositories('all')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('repos'),
            params={'type': 'all', 'per_page': 100},
            headers={}
        )

    def test_teams(self):
        """Show that one can iterate over an organization's teams."""
        i = self.instance.teams()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('teams'),
            params={'per_page': 100},
            headers={}
        )

    def test_teams_requires_auth(self):
        """Show that one must be authenticated to retrieve an org's teams."""
        self.session.has_auth.return_value = False

        with pytest.raises(GitHubError):
            self.instance.teams()

    def test_invitations(self):
        """Show that one can iterate over outstanding invitations."""
        i = self.instance.invitations()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('invitations'),
            params={'per_page': 100},
            headers={'Accept': 'application/vnd.github.korra-preview'}
        )
