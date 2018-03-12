import pytest

from github3 import GitHubError
from github3.orgs import Team

from . import helper

url_for = helper.create_url_helper('https://api.github.com/teams/1')

get_team_example_data = helper.create_example_data_helper('orgs_team_example')


class TestTeam(helper.UnitHelper):
    described_class = Team
    example_data = get_team_example_data()

    def test_add_member(self):
        """Show that one can add a member to an organization team."""
        self.instance.add_member('user')

        self.session.put.assert_called_once_with(url_for('members/user'))

    def test_add_repository(self):
        """Show that one can add a repository to an organization team."""
        self.instance.add_repository('name-of-repo')

        self.put_called_with(url_for('repos/name-of-repo'),
                             data={})

        self.instance.add_repository('name-of-repo', permission='push')

        self.put_called_with(url_for('repos/name-of-repo'),
                             data={'permission': 'push'})

    def test_delete(self):
        """Show that a user can delete an organization team."""
        self.instance.delete()

        self.session.delete.assert_called_once_with(url_for())

    def test_edit(self):
        """Show that a user can edit a team."""
        self.instance.edit('name', 'admin')

        self.patch_called_with(url_for(),
                               data={'name': 'name', 'permission': 'admin'})

    def test_has_repository(self):
        """Show that a user can check if a team has access to a repository."""
        self.instance.has_repository('org/repo')

        self.session.get.assert_called_once_with(url_for('repos/org/repo'))

    def test_is_member(self):
        """Show that a user can check if another user is a team member."""
        self.instance.is_member('username')

        self.session.get.assert_called_once_with(url_for('members/username'))

    def test_remove_member(self):
        """Show that a user can check if another user is a team member."""
        self.instance.remove_member('username')

        self.session.delete.assert_called_once_with(
            url_for('members/username')
        )

    def test_remove_repository(self):
        """Show that a user can remove a repository from a team."""
        self.instance.remove_repository('repo')

        self.session.delete.assert_called_once_with(url_for('/repos/repo'))


class TestTeamRequiresAuth(helper.UnitRequiresAuthenticationHelper):
    described_class = Team
    example_data = get_team_example_data()

    def test_add_member_requires_auth(self):
        """Show that adding a repo to a team requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.add_member('user')

    def test_add_repository_requires_auth(self):
        """Show that adding a repo to a team requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.add_repository('repo')

    def test_delete_requires_auth(self):
        """Show that deleteing a team requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.delete()

    def test_edit_requires_auth(self):
        """Show that editing a team requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.edit('name')

    def test_has_repository_requires_auth(self):
        """Show that checking a team's access to a repo needs auth."""
        with pytest.raises(GitHubError):
            self.instance.has_repository('org/repo')

    def test_is_member_requires_auth(self):
        """Show that checking a user's team membership requires auth."""
        with pytest.raises(GitHubError):
            self.instance.is_member('user')

    def test_remove_member_requires_auth(self):
        """Show that removing a team member requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.remove_member('user')

    def test_remove_repository_requires_auth(self):
        """Show that removing a repo from a team requires authentication."""
        with pytest.raises(GitHubError):
            self.instance.remove_repository('repo')


class TestTeamIterator(helper.UnitIteratorHelper):
    described_class = Team
    example_data = get_team_example_data()

    def test_members(self):
        """Show that one can iterate over all members of a Team."""
        i = self.instance.members()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('members'),
            params={'per_page': 100},
            headers={}
        )

    def test_members_roles(self):
        """Show that one can iterate of all maintainers of a Team."""
        i = self.instance.members(role='maintainer')
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('members'),
            params={'per_page': 100, 'role': 'maintainer'},
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

    def test_members_requires_auth(self):
        """Show that one needs to authenticate to get team members."""
        self.session.has_auth.return_value = False

        with pytest.raises(GitHubError):
            self.instance.members()

    def test_repositories(self):
        """Show that one can iterate over an organization's repositories."""
        i = self.instance.repositories()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('repos'),
            params={'per_page': 100},
            headers={'Accept': 'application/vnd.github.ironman-preview+json'}
        )
