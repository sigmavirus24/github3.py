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
        github3.all_events()
        self.gh.all_events.assert_called_once_with(-1, None)

    def test_public_gists(self):
        github3.public_gists()
        self.gh.public_gists.assert_called_once_with(-1, None)

    def test_all_repositories(self):
        github3.all_repositories()
        # TODO(Ian): When you fix GitHub, fix this test too
        self.gh.all_repositories.assert_called_once_with(-1, None)

    def test_all_users(self):
        github3.all_users()
        # TODO(Ian): Fix this when GitHub changes
        self.gh.all_users.assert_called_once_with(-1, None)

    def test_authorize(self):
        args = ('login',  'password', ['scope'], 'note', 'url.com', '', '')
        with mock.patch('github3.api.GitHub') as gh:
            github3.authorize(*args)
            gh().authorize.assert_called_once_with(*args)

    def test_create_gist(self):
        args = ('description', {'files': ['file']})
        github3.create_gist(*args)
        self.gh.create_gist.assert_called_once_with(*args)

    def test_enterprise_login(self):
        args = ('login', 'password', None, 'https://url.com/', None)
        with mock.patch.object(github3.GitHubEnterprise, 'login') as login:
            g = github3.enterprise_login(*args)
            assert isinstance(g, github3.GitHubEnterprise)
            login.assert_called_once_with('login', 'password', None, None)

    def test_followers_of(self):
        github3.followers_of('login')
        self.gh.followers_of.assert_called_with('login', -1, None)

    def test_followed_by(self):
        github3.followed_by('login')
        self.gh.followed_by.assert_called_with('login', -1, None)

    def test_gist(self):
        gist_id = 123
        github3.gist(gist_id)
        self.gh.gist.assert_called_once_with(gist_id)

    def test_gists_by(self):
        github3.gists_by('username')
        self.gh.gists_by.assert_called_once_with('username', -1, None)

    def test_gitignore_template(self):
        language = 'Python'
        github3.gitignore_template(language)
        self.gh.gitignore_template.assert_called_once_with(language)

    def test_gitignore_templates(self):
        github3.gitignore_templates()
        assert self.gh.gitignore_templates.called is True

    def test_issue(self):
        github3.issue('sigmavirus24', 'github3.py', 100)
        self.gh.issue.assert_called_with('sigmavirus24', 'github3.py', 100)

    def test_login(self):
        args = ('login', 'password', None, None)
        with mock.patch.object(github3.GitHub, 'login') as login:
            g = github3.login(*args)
            assert isinstance(g, github3.GitHub)
            assert not isinstance(g, github3.GitHubEnterprise)
            login.assert_called_once_with(*args)

    def test_markdown(self):
        github3.markdown('text', '', '', False)
        self.gh.markdown.assert_called_once_with('text', '', '', False)

    def test_octocat(self):
        github3.octocat()
        self.gh.octocat.assert_called_once_with(None)

    def test_organization(self):
        github3.organization('orgname')
        self.gh.organization.assert_called_once_with('orgname')

    def test_organizations_with(self):
        args = ('login', -1, None)
        github3.organizations_with(*args)
        self.gh.organizations_with.assert_called_with(*args)

    def test_pull_request(self):
        github3.pull_request('sigmavirus24', 'github3.py', 24)
        self.gh.pull_request.assert_called_once_with('sigmavirus24',
                                                     'github3.py',
                                                     24)

    def test_rate_limit(self):
        github3.rate_limit()
        self.gh.rate_limit.assert_called_once_with()

    def test_repository(self):
        github3.repository('sigmavirus24', 'github3.py')
        self.gh.repository.assert_called_once_with('sigmavirus24',
                                                   'github3.py')

    def test_repository_issues(self):
        args = ('owner', 'repository', None, None, None, None, None, None,
                None, None, -1, None)
        github3.repository_issues(*args)
        self.gh.repository_issues.assert_called_with(*args)

    def test_repositories_by(self):
        args = ('login', None, None, None, -1, None)
        github3.repositories_by('login')
        self.gh.repositories_by.assert_called_with(*args)

    def test_starred(self):
        github3.starred_by('login')
        self.gh.starred_by.assert_called_with('login', -1, None)

    def test_subcriptions_for(self):
        github3.subscriptions_for('login')
        self.gh.subscriptions_for.assert_called_with('login', -1, None)

    def test_user(self):
        github3.user('sigmavirus24')
        self.gh.user.assert_called_once_with('sigmavirus24')

    def test_zen(self):
        github3.zen()
        assert self.gh.zen.called is True
