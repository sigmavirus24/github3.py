import github3
import mock
import unittest


class TestAPI(unittest.TestCase):
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

    def test_all_repos(self):
        github3.all_repos()
        # TODO(Ian): When you fix GitHub, fix this test too
        self.gh.all_repos.assert_called_once_with(-1, None)

    def test_all_users(self):
        github3.all_users()
        # TODO(Ian): Fix this when GitHub changes
        self.gh.all_users.assert_called_once_with(-1, None)

    def test_authorize(self):
        args = ('login',  'password', ['scope'], 'note', 'url.com', '', '')
        github3.authorize(*args)
        self.gh.authorize.assert_called_once_with(*args)

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

    def test_login(self):
        args = ('login', 'password', None, None)
        with mock.patch.object(github3.GitHub, 'login') as login:
            g = github3.login(*args)
            assert isinstance(g, github3.GitHub)
            assert not isinstance(g, github3.GitHubEnterprise)
            login.assert_called_once_with(*args)

    def test_organizations(self):
        args = ('login', -1, None)
        github3.organizations(*args)
        self.gh.organizations.assert_called_with(*args)

    def test_repository_issues(self):
        args = ('owner', 'repository', None, None, None, None, None, None,
                None, None, -1, None)
        github3.repository_issues(*args)
        self.gh.repository_issues.assert_called_with(*args)

    def test_starred(self):
        github3.starred_by('login')
        self.gh.starred_by.assert_called_with('login', -1, None)

    def test_subcriptions_for(self):
        github3.subscriptions_for('login')
        self.gh.subscriptions_for.assert_called_with('login', -1, None)

    def test_user_repos(self):
        args = ('login', None, None, None, -1, None)
        github3.user_repos('login')
        self.gh.user_repos.assert_called_with(*args)
