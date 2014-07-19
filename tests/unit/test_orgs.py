import pytest

from github3 import GitHubError
from github3.orgs import Organization

from .helper import UnitHelper, UnitIteratorHelper


def url_for(path=''):
    """Simple function to generate URLs with the base Org URL."""
    if path:
        path = '/' + path.strip('/')
    return 'https://api.github.com/orgs/hapy' + path


class TestOrganization(UnitHelper):
    described_class = Organization
    example_data = {
        'login': 'hapy',
        'id': 1,
        'url': 'https://api.github.com/orgs/hapy',
        'avatar_url': 'https://github.com/images/error/octocat_happy.gif',
        'name': 'github',
        'company': 'GitHub',
        'blog': 'https://github.com/blog',
        'location': 'San Francisco',
        'email': 'octocat@github.com',
        'public_repos': 2,
        'public_gists': 1,
        'followers': 20,
        'following': 0,
        'html_url': 'https://github.com/hapy',
        'created_at': '2008-01-14T04:33:35Z',
        'type': 'Organization'
    }

    def test_add_member(self):
        """Show that an authenticated user can add a member to an org."""
        self.instance.add_member('user', 10)

        self.session.put.assert_called_once_with(
            'https://api.github.com/teams/10/members/user'
        )

    def test_add_member_requires_auth(self):
        """Show that one must be authenticated to add a member to an org."""
        self.session.has_auth.return_value = False

        with pytest.raises(GitHubError):
            self.instance.add_member('user', 10)

    def test_add_repository(self):
        """Show that one can add a repository to an organization."""
        self.instance.add_repository('name-of-repo', 10)

        self.session.put.assert_called_once_with(
            'https://api.github.com/teams/10/repos/name-of-repo'
        )

    def test_add_repository_requires_auth(self):
        """Show that one must be authenticated to add a repo to an org."""
        self.session.has_auth.return_value = False

        with pytest.raises(GitHubError):
            self.instance.add_repository('foo', 10)


class TestOrganizationIterator(UnitIteratorHelper):
    described_class = Organization

    example_data = {
        'url': url_for()
    }

    def test_events(self):
        """Show that one can iterate over an organization's events."""
        i = self.instance.events()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('events'),
            params={'per_page': 100},
            headers={}
        )

    def test_members(self):
        """Show that one can iterate over all members."""
        i = self.instance.members()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('members'),
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
