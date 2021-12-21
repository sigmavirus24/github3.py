"""Unit tests for github3.api."""
import unittest.mock

import github3


class TestAPI(unittest.TestCase):

    """All tests for the github3.api module."""

    def test_enterprise_login(self):
        """Show that github3.enterprise_login returns GitHubEnterprise."""
        args = ("login", "password", None, "https://url.com/", None)
        with unittest.mock.patch.object(
            github3.GitHubEnterprise, "login"
        ) as login:
            g = github3.enterprise_login(*args)
            assert isinstance(g, github3.GitHubEnterprise)
            login.assert_called_once_with("login", "password", None, None)

    def test_login(self):
        """Show that github3.login proxies to GitHub."""
        args = ("login", "password", None, None)
        with unittest.mock.patch.object(github3.GitHub, "login") as login:
            g = github3.login(*args)
            assert isinstance(g, github3.GitHub)
            assert not isinstance(g, github3.GitHubEnterprise)
            login.assert_called_once_with(*args)
