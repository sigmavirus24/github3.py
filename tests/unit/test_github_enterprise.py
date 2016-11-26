import github3
from github3.github import GitHubEnterprise
from .helper import UnitHelper, create_example_data_helper

get_example_user = create_example_data_helper('user_example')

example_data = get_example_user()

base_url = 'https://ghe.example.com/'


def _build_url(_, *args, **kwargs):
    return github3.session.GitHubSession().build_url(
        base_url=base_url + 'api/v3', *args, **kwargs)


class TestGitHubEnterprise(UnitHelper):
    described_class = GitHubEnterprise
    example_data = base_url

    def create_instance_of_described_class(self):
        instance = self.described_class(self.example_data)
        instance.session = self.session

        return instance

    def after_setup(self):
        self.described_class._build_url = _build_url

    def url_for(self, path=''):
        """Generate URLs with the base GitHubEnterprise URL."""
        return base_url + 'api/v3/' + path.strip('/')

    def test_create_user(self):
        """Show that an admin can ask for user creation."""
        self.instance.create_user('login_test', 'email_test')

        self.post_called_with(
            self.url_for('admin/users'),
            data={'login': 'login_test', 'email': 'email_test'}
        )


class TestUserAdministration(UnitHelper):
    described_class = github3.users.User
    example_data = example_data
    # Remove the end of the string starting with 'users'
    base_url = example_data['url'][:example_data['url'].rfind('users')]

    def url_for_user(self, path=''):
        return self.base_url + 'users/' + example_data['login'] + path

    def url_for_admin(self, path=''):
        return (self.base_url + 'admin/users/' + str(example_data['login']) +
                path)

    def test_delete_user(self):
        """Show that an admin can ask for user deletion."""
        self.instance.delete()
        self.session.delete.assert_called_once_with(self.url_for_admin())

    def test_rename_user(self):
        """Show that an admin can ask for user renaming."""
        self.instance.rename('new_login')
        self.session.patch.assert_called_once_with(self.url_for_admin(),
                                                   data={'login': 'new_login'})

    def test_impersonate(self):
        """Show that an admin can ask for an impersonation token for a user."""
        self.instance.impersonate(scopes=['repo', 'user'])
        self.post_called_with(self.url_for_admin('/authorizations'),
                              data={'scopes': ['repo', 'user']})

    def test_revoke_impersonation(self):
        """Show that an admin can revoke impersonation tokens for a user."""
        self.instance.revoke_impersonation()
        self.session.delete.assert_called_once_with(
            self.url_for_admin('/authorizations'))

    def test_promote(self):
        """Show that an admin can promote a specific user."""
        self.instance.promote()
        self.session.put.assert_called_once_with(
            self.url_for_user('/site_admin'))

    def test_demote(self):
        """Show that an admin can demote another admin."""
        self.instance.demote()
        self.session.delete.assert_called_once_with(
            self.url_for_user('/site_admin'))

    def test_suspend(self):
        """Show that an admin can suspend a user."""
        self.instance.suspend()
        self.session.put.assert_called_once_with(
            self.url_for_user('/suspended'))

    def test_unsuspend(self):
        """Show that an admin can unsuspend a user."""
        self.instance.unsuspend()
        self.session.delete.assert_called_once_with(
            self.url_for_user('/suspended'))
