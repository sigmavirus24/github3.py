"""Unit tests for github4.api."""
import unittest.mock

import github4


class TestAPI(unittest.TestCase):

    """All tests for the github4.api module."""

    def test_enterprise_login(self):
        """Show that github4.enterprise_login returns GitHubEnterprise."""
        args = ("login", "password", None, "https://url.com/", None)
        with unittest.mock.patch.object(github4.GitHubEnterprise, "login") as login:
            g = github4.enterprise_login(*args)
            assert isinstance(g, github4.GitHubEnterprise)
            login.assert_called_once_with("login", "password", None, None)

    def test_login(self):
        """Show that github4.login proxies to GitHub."""
        args = ("login", "password", None, None)
        with unittest.mock.patch.object(github4.GitHub, "login") as login:
            g = github4.login(*args)
            assert isinstance(g, github4.GitHub)
            assert not isinstance(g, github4.GitHubEnterprise)
            login.assert_called_once_with(*args)
