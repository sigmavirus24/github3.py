"""Unit tests for github3.api."""
import github3
import unittest

from .helper import mock


class TestAPI(unittest.TestCase):

    """All tests for the github3.api module."""

    def setUp(self):
        self.mocked_github = mock.patch('github3.api.gh',
                                        autospec=github3.GitHub)
        self.gh = self.mocked_github.start()

    def tearDown(self):
        self.mocked_github.stop()

    def test_all_events(self):
        """Show that github3.all_events proxies to GitHub."""
        github3.all_events()
        self.gh.all_events.assert_called_once_with(-1, None)

    def test_public_gists(self):
        """Show that github3.public_gists proxies to GitHub."""
        github3.public_gists()
        self.gh.public_gists.assert_called_once_with(-1, None)

    def test_all_repositories(self):
        """Show that github3.all_repositories proxies to GitHub."""
        github3.all_repositories()
        # TODO(Ian): When you fix GitHub, fix this test too
        self.gh.all_repositories.assert_called_once_with(-1, None)

    def test_all_users(self):
        """Show that github3.all_users proxies to GitHub."""
        github3.all_users()
        # TODO(Ian): Fix this when GitHub changes
        self.gh.all_users.assert_called_once_with(-1, None)

    def test_authorize(self):
        """Show that github3.authorize proxies to GitHub."""
        args = ('login', 'password', ['scope'], 'note', 'url.com', '', '')
        with mock.patch('github3.api.GitHub') as gh:
            github3.authorize(*args)
            gh().authorize.assert_called_once_with(*args)

    def test_authorize_with_github_argument(self):
        """Show that github3.authorize can use an existing GitHub object."""
        args = ('login', 'password', ['scope'], 'note', 'url.com', '', '')
        github = mock.Mock(spec_set=github3.GitHub)
        with mock.patch('github3.api.GitHub') as gh:
            github3.authorize(*args, github=github)
            gh().assert_not_called()
            github.authorize.assert_called_once_with(*args)

    def test_create_gist(self):
        """Show that github3.create_gist proxies to GitHub."""
        args = ('description', {'files': ['file']})
        github3.create_gist(*args)
        self.gh.create_gist.assert_called_once_with(*args)

    def test_enterprise_login(self):
        """Show that github3.enterprise_login returns GitHubEnterprise."""
        args = ('login', 'password', None, 'https://url.com/', None)
        with mock.patch.object(github3.GitHubEnterprise, 'login') as login:
            g = github3.enterprise_login(*args)
            assert isinstance(g, github3.GitHubEnterprise)
            login.assert_called_once_with('login', 'password', None, None)

    def test_followers_of(self):
        """Show that github3.followers_of proxies to GitHub."""
        github3.followers_of('login')
        self.gh.followers_of.assert_called_with('login', -1, None)

    def test_followed_by(self):
        """Show that github3.followed_by proxies to GitHub."""
        github3.followed_by('login')
        self.gh.followed_by.assert_called_with('login', -1, None)

    def test_gist(self):
        """Show that github3.gist proxies to GitHub."""
        gist_id = 123
        github3.gist(gist_id)
        self.gh.gist.assert_called_once_with(gist_id)

    def test_gists_by(self):
        """Show that github3.gists_by proxies to GitHub."""
        github3.gists_by('username')
        self.gh.gists_by.assert_called_once_with('username', -1, None)

    def test_gitignore_template(self):
        """Show that github3.gitignore_template proxies to GitHub."""
        language = 'Python'
        github3.gitignore_template(language)
        self.gh.gitignore_template.assert_called_once_with(language)

    def test_gitignore_templates(self):
        """Show that github3.gitignore_templates proxies to GitHub."""
        github3.gitignore_templates()
        assert self.gh.gitignore_templates.called is True

    def test_issue(self):
        """Show that github3.issue proxies to GitHub."""
        github3.issue('sigmavirus24', 'github3.py', 100)
        self.gh.issue.assert_called_with('sigmavirus24', 'github3.py', 100)

    def test_login(self):
        """Show that github3.login proxies to GitHub."""
        args = ('login', 'password', None, None)
        with mock.patch.object(github3.GitHub, 'login') as login:
            g = github3.login(*args)
            assert isinstance(g, github3.GitHub)
            assert not isinstance(g, github3.GitHubEnterprise)
            login.assert_called_once_with(*args)

    def test_markdown(self):
        """Show that github3.markdown proxies to GitHub."""
        github3.markdown('text', '', '', False)
        self.gh.markdown.assert_called_once_with('text', '', '', False)

    def test_octocat(self):
        """Show that github3.octocat proxies to GitHub."""
        github3.octocat()
        self.gh.octocat.assert_called_once_with(None)

    def test_organization(self):
        """Show that github3.organization proxies to GitHub."""
        github3.organization('orgname')
        self.gh.organization.assert_called_once_with('orgname')

    def test_organizations_with(self):
        """Show that github3.organizations_with proxies to GitHub."""
        args = ('login', -1, None)
        github3.organizations_with(*args)
        self.gh.organizations_with.assert_called_with(*args)

    def test_pull_request(self):
        """Show that github3.pull_request proxies to GitHub."""
        github3.pull_request('sigmavirus24', 'github3.py', 24)
        self.gh.pull_request.assert_called_once_with('sigmavirus24',
                                                     'github3.py',
                                                     24)

    def test_rate_limit(self):
        """Show that github3.rate_limit proxies to GitHub."""
        github3.rate_limit()
        self.gh.rate_limit.assert_called_once_with()

    def test_repository(self):
        """Show that github3.repository proxies to GitHub."""
        github3.repository('sigmavirus24', 'github3.py')
        self.gh.repository.assert_called_once_with('sigmavirus24',
                                                   'github3.py')

    def test_issues_on(self):
        """Show that github3.issues_on proxies to GitHub."""
        args = ('owner', 'repository', None, None, None, None, None, None,
                None, None, -1, None)
        github3.issues_on(*args)
        self.gh.issues_on.assert_called_with(*args)

    def test_repositories_by(self):
        """Show that github3.repositories_by proxies to GitHub."""
        args = ('login', None, None, None, -1, None)
        github3.repositories_by('login')
        self.gh.repositories_by.assert_called_with(*args)

    def test_starred(self):
        """Show that github3.starred proxies to GitHub."""
        github3.starred_by('login')
        self.gh.starred_by.assert_called_with('login', -1, None)

    def test_subcriptions_for(self):
        """Show that github3.subscriptions_for proxies to GitHub."""
        github3.subscriptions_for('login')
        self.gh.subscriptions_for.assert_called_with('login', -1, None)

    def test_user(self):
        """Show that github3.user proxies to GitHub."""
        github3.user('sigmavirus24')
        self.gh.user.assert_called_once_with('sigmavirus24')

    def test_zen(self):
        """Show that github3.zen proxies to GitHub."""
        github3.zen()
        assert self.gh.zen.called is True
