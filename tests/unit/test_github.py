from github3.github import GitHub

from .helper import UnitHelper, UnitIteratorHelper


def url_for(path=''):
    return 'https://api.github.com/' + path.strip('/')


class TestGitHub(UnitHelper):
    described_class = GitHub
    example_data = None

    def test_two_factor_login(self):
        self.instance.login('username', 'password',
                            two_factor_callback=lambda *args: 'foo')

    def test_can_login_without_two_factor_callback(self):
        self.instance.login('username', 'password')
        self.instance.login(token='token')


class TestGitHubIterators(UnitIteratorHelper):
    described_class = GitHub
    example_data = None

    def test_user_repos(self):
        """Test that one can iterate over a user's repositories."""
        i = self.instance.user_repos('sigmavirus24')

        # Get the next item from the iterator
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('users/sigmavirus24/repos'),
            params={'per_page': 100},
            headers={}
        )

    def test_user_repos_with_type(self):
        """
        Test that one can iterate over a user's repositories with a type.
        """
        i = self.instance.user_repos('sigmavirus24', 'all')

        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('users/sigmavirus24/repos'),
            params={'per_page': 100, 'type': 'all'},
            headers={}
        )
