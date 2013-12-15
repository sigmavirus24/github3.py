import github3
from unittest import TestCase
from mock import patch, NonCallableMock


class TestAPI(TestCase):
    def setUp(self):
        self.mock = patch('github3.api.gh', autospec=github3.GitHub)
        self.gh = self.mock.start()

    def tearDown(self):
        self.mock.stop()

    def test_authorize(self):
        args = ('login', 'password', ['scope1'], 'note', 'note_url.com', '',
                '')
        github3.authorize(*args)
        self.gh.authorize.assert_called_with(*args)

    def test_login(self):
        args = ('login', 'password', None)
        with patch.object(github3.api.GitHub, 'login') as login:
            g = github3.login(*args)
            assert isinstance(g, github3.github.GitHub)
            assert not isinstance(g, github3.github.GitHubEnterprise)
            login.assert_called_with(*args)

    def test_enterprise_login(self):
        args = ('login', 'password', None, 'http://ghe.invalid/')
        with patch.object(github3.api.GitHubEnterprise, 'login') as login:
            g = github3.login(*args)
            assert isinstance(g, github3.github.GitHubEnterprise)
            login.assert_called_with(*args[:3])

    def test_gist(self):
        args = (123,)
        github3.gist(*args)
        self.gh.gist.assert_called_with(*args)

    def test_gitignore_template(self):
        args = ('Python',)
        github3.gitignore_template(*args)
        self.gh.gitignore_template.assert_called_with(*args)

    def test_gitignore_templates(self):
        github3.gitignore_templates()
        assert self.gh.gitignore_templates.called is True

    def test_iter_all_repos(self):
        github3.iter_all_repos()
        self.gh.iter_all_repos.assert_called_with(-1, None)

    def test_iter_all_users(self):
        github3.iter_all_users()
        self.gh.iter_all_users.assert_called_with(-1, None)

    def test_iter_events(self):
        github3.iter_events()
        self.gh.iter_events.assert_called_with(-1, None)

    def test_iter_followers(self):
        github3.iter_followers('login')
        self.gh.iter_followers.assert_called_with('login', -1, None)

    def test_iter_following(self):
        github3.iter_following('login')
        self.gh.iter_following.assert_called_with('login', -1, None)

    def test_iter_gists(self):
        github3.iter_gists()
        self.gh.iter_gists.assert_called_with(None, -1, None)

    def test_iter_repo_issues(self):
        args = ('owner', 'repository', None, None, None, None, None, None,
                None, None, -1, None)
        github3.iter_repo_issues(*args)
        self.gh.iter_repo_issues.assert_called_with(*args)

        github3.iter_repo_issues(None, None)

    def test_iter_orgs(self):
        args = ('login', -1, None)
        github3.iter_orgs(*args)
        self.gh.iter_orgs.assert_called_with(*args)

    def test_iter_user_repos(self):
        args = ('login', None, None, None, -1, None)
        github3.iter_user_repos('login')
        self.gh.iter_user_repos.assert_called_with(*args)

        github3.iter_user_repos(None)

    def test_iter_starred(self):
        github3.iter_starred('login')
        self.gh.iter_starred.assert_called_with('login', -1, None)

    def test_iter_subcriptions(self):
        github3.iter_subscriptions('login')
        self.gh.iter_subscriptions.assert_called_with('login', -1, None)

    def test_create_gist(self):
        args = ('description', {'files': ['files']})
        github3.create_gist(*args)
        self.gh.create_gist.assert_called_with(*args)

    def test_issue(self):
        args = ('owner', 'repo', 1)
        github3.issue(*args)
        self.gh.issue.assert_called_with(*args)

    def test_markdown(self):
        args = ('text', '', '', False)
        github3.markdown(*args)
        self.gh.markdown.assert_called_with(*args)

    def test_octocat(self):
        github3.octocat()
        assert self.gh.octocat.called is True

    def test_organization(self):
        github3.organization('login')
        self.gh.organization.assert_called_with('login')

    def test_pull_request(self):
        args = ('owner', 'repo', 1)
        github3.pull_request(*args)
        self.gh.pull_request.assert_called_with(*args)

    def test_repository(self):
        args = ('owner', 'repo')
        github3.repository(*args)
        self.gh.repository.assert_called_with(*args)

    def test_user(self):
        github3.user('login')
        self.gh.user.assert_called_with('login')

    def test_rate_limit(self):
        github3.rate_limit()
        self.gh.rate_limit.assert_called_once_with()

    def test_ratelimit_remaining(self):
        # This prevents a regression in the API
        # See 81c800658db43f86419b9c0764fc16aad3d60007
        self.gh.ratelimit_remaining = NonCallableMock()
        github3.ratelimit_remaining()

    def test_zen(self):
        github3.zen()
        assert self.gh.zen.called is True
