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

    def test_login(self):
        args = ('login', 'password', None, None)
        with mock.patch.object(github3.GitHub, 'login') as login:
            g = github3.login(*args)
            assert isinstance(g, github3.GitHub)
            assert not isinstance(g, github3.GitHubEnterprise)
            login.assert_called_once_with(*args)
