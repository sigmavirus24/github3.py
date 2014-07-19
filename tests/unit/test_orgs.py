import pytest

from github3 import GitHubError
from github3.orgs import Organization

from .helper import UnitIteratorHelper


def url_for(path=''):
    """Simple function to generate URLs with the base Org URL."""
    if path:
        path = '/' + path.strip('/')
    return 'https://api.github.com/orgs/hapy' + path


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
