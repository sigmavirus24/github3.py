import github3
from unittest import TestCase
from mock import patch, NonCallableMock


class TestAPI(TestCase):
    def setUp(self):
        self.mock = patch('github3.api.gh', autospec=github3.GitHub)
        self.gh = self.mock.start()

    def tearDown(self):
        self.mock.stop()

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
