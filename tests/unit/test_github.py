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

    def test_revoke_authorization(self):
        self.instance.set_client_id('key', 'secret')
        self.instance.revoke_authorization('access_token')
        self.session.delete.assert_called_once_with(
            'https://api.github.com/applications/key/tokens/access_token',
            auth=('key', 'secret'),
            params={'client_id': None, 'client_secret': None}
        )

    def test_revoke_authorizations(self):
        self.instance.set_client_id('key', 'secret')
        self.instance.revoke_authorizations()
        self.session.delete.assert_called_once_with(
            'https://api.github.com/applications/key/tokens',
            auth=('key', 'secret'),
            params={'client_id': None, 'client_secret': None}
        )
