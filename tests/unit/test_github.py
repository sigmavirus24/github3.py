from github3.github import GitHub

from .helper import UnitHelper


class TestGitHub(UnitHelper):
    described_class = GitHub
    example_data = None

    def test_two_factor_login(self):
        self.instance.login('username', 'password',
                            two_factor_callback=lambda *args: 'foo')

    def test_can_login_without_two_factor_callback(self):
        self.instance.login('username', 'password')
        self.instance.login(token='token')


class TestGitHubAuthorizations(UnitHelper):
    described_class = GitHub
    example_data = None

    def create_session_mock(self, *args):
        session = super(TestGitHubAuthorizations,
                        self).create_session_mock(*args)
        session.retrieve_client_credentials.return_value = ('id', 'secret')
        return session

    def test_revoke_authorization(self):
        """Test that GitHub#revoke_authorization calls the expected methods.

        It should use the session's delete and temporary_basic_auth methods.
        """
        self.instance.revoke_authorization('access_token')
        self.session.delete.assert_called_once_with(
            'https://api.github.com/applications/id/tokens/access_token',
            params={'client_id': None, 'client_secret': None}
        )
        self.session.temporary_basic_auth.assert_called_once_with(
            'id', 'secret'
        )

    def test_revoke_authorizations(self):
        """Test that GitHub#revoke_authorizations calls the expected methods.

        It should use the session's delete and temporary_basic_auth methods.
        """
        self.instance.revoke_authorizations()
        self.session.delete.assert_called_once_with(
            'https://api.github.com/applications/id/tokens',
            params={'client_id': None, 'client_secret': None}
        )
        self.session.temporary_basic_auth.assert_called_once_with(
            'id', 'secret'
        )
