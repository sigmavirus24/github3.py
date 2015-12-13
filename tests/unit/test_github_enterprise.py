import pytest

from github3.github import GitHubEnterprise
import github3

from .helper import UnitHelper

example_data = {
    "login": "octocat",
    "id": 1,
    "avatar_url": "https://github.com/images/error/octocat_happy.gif",
    "gravatar_id": "somehexcode",
    "url": "https://api.github.com/users/octocat",
    "html_url": "https://github.com/octocat",
    "followers_url": "https://api.github.com/users/octocat/followers",
    "following_url": ("https://api.github.com/users/octocat/following"
                      "{/other_user}"),
    "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
    "starred_url": ("https://api.github.com/users/octocat/starred"
                    "{/owner}{/repo}"),
    "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
    "organizations_url": "https://api.github.com/users/octocat/orgs",
    "repos_url": "https://api.github.com/users/octocat/repos",
    "events_url": "https://api.github.com/users/octocat/events{/privacy}",
    "received_events_url": ("https://api.github.com/users/octocat/"
                            "received_events"),
    "type": "User",
    "site_admin": False,
    "name": "monalisa octocat",
    "company": "GitHub",
    "blog": "https://github.com/blog",
    "location": "San Francisco",
    "email": "octocat@github.com",
    "hireable": False,
    "bio": "There once was...",
    "public_repos": 2,
    "public_gists": 1,
    "followers": 20,
    "following": 0,
    "created_at": "2008-01-14T04:33:35Z",
    "updated_at": "2008-01-14T04:33:35Z"
}


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


class TestUserAdministration(UnitHelper):
    described_class = github3.users.User
    example_data = example_data.copy()
    # Remove the end of the string starting with 'users'
    base_url = example_data['url'][:example_data['url'].rfind('users')]

    def url_for_user(self, path=''):
        return self.base_url + 'users/' + example_data['login'] + path

    def url_for_admin(self, path=''):
        return self.base_url + 'admin/users/' + str(example_data['id']) + path

    def test_delete_user(self):
        """Show that an admin can ask for user deletion."""
        self.instance.delete()
        self.session.delete.assert_called_once_with(self.url_for_admin())

    def test_rename_user(self):
        """Show that an admin can ask for user renaming."""
        self.instance.rename('new_login')
        self.session.patch.assert_called_once_with(self.url_for_admin(), data={'login': 'new_login'})

    def test_impersonate(self):
        """Show that an admin can ask for an impersonation token for a specific user."""
        self.instance.impersonate(scopes=['repo', 'user'])
        self.post_called_with(self.url_for_admin('/authorizations'), data={'scopes': ['repo', 'user']})

    def test_revoke_impersonation(self):
        """Show that an admin can revoke impersonation tokens for a specific user."""
        self.instance.revoke_impersonation()
        self.session.delete.assert_called_once_with(self.url_for_admin('/authorizations'))

    def test_promote(self):
        """Show that an admin can promote a specific user."""
        self.instance.promote()
        self.session.put.assert_called_once_with(self.url_for_user('/site_admin'))

    def test_demote(self):
        """Show that an admin can demote another admin."""
        self.instance.demote()
        self.session.delete.assert_called_once_with(self.url_for_user('/site_admin'))

    def test_suspend(self):
        """Show that an admin can suspend a user."""
        self.instance.suspend()
        self.session.put.assert_called_once_with(self.url_for_user('/suspended'))

    def test_unsuspend(self):
        """Show that an admin can unsuspend a user."""
        self.instance.unsuspend()
        self.session.delete.assert_called_once_with(self.url_for_user('/suspended'))
