import pytest

from github3.github import GitHubEnterprise

from .helper import UnitHelper


class TestGitHubEnterprise(UnitHelper):
    described_class = GitHubEnterprise
    base_url = 'https://ghe.example.com/'
    example_data = base_url

    def url_for(self, path=''):
        """Simple function to generate URLs with the base GitHubEnterprise URL."""
        return self.base_url + 'api/v3/' + path.strip('/')

    def test_create_user(self):
        """Show that an admin can ask for user creation."""
        self.instance.create_user('login_test', 'email_test')

        self.post_called_with(
            self.url_for('admin/users'),
            data={'login': 'login_test', 'email': 'email_test'}
        )
