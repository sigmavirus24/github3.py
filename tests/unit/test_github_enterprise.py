import pytest

from github3.github import GitHubEnterprise
import github3

from .helper import UnitHelper


class TestGitHubEnterprise(UnitHelper):
    described_class = GitHubEnterprise
    base_url = 'https://ghe.example.com/'
    example_data = base_url

    def create_instance_of_described_class(self):
        instance = self.described_class(self.example_data)
        instance.session = self.session

        return instance

    def after_setup(self):
        self.described_class._build_url = lambda _, *args, **kwargs: github3.session.GitHubSession().build_url(
            base_url=self.base_url + 'api/v3', *args, **kwargs)

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
