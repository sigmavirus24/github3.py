"""Unit tests for the auths module."""
import github3

from . import helper

url_for = helper.create_url_helper('https://api.github.com/authorizations/1')


class TestAuthorization(helper.UnitHelper):

    """Authorization unit tests."""

    described_class = github3.auths.Authorization
    get_auth_example_data = helper.create_example_data_helper(
        'authorization_example'
    )
    example_data = get_auth_example_data()

    def test_add_scopes(self):
        """Test the request to add scopes to an authorization."""
        self.instance.add_scopes(['scope-one', 'scope-two'])

        self.post_called_with(url_for(''), data={
            'add_scopes': ['scope-one', 'scope-two'],
        })

    def test_delete(self):
        """Test the request to delete an authorization."""
        self.instance.delete()

        self.session.delete.assert_called_once_with(url_for(''))

    def test_remove_scopes(self):
        """Test the request to remove scopes from an authorization."""
        self.instance.remove_scopes(['scope-one', 'scope-two', 'scope-three'])

        self.post_called_with(url_for(''), data={
            'rm_scopes': ['scope-one', 'scope-two', 'scope-three'],
        })

    def test_replace_scopes(self):
        """Test the request to replace the scopes on an authorization."""
        self.instance.replace_scopes(['scope-one', 'scope-two', 'scope-three'])

        self.post_called_with(url_for(''), data={
            'scopes': ['scope-one', 'scope-two', 'scope-three'],
        })


class TestAuthorizationRequiresAuth(helper.UnitRequiresAuthenticationHelper):

    """Test methods that require authentication on Authorization."""

    described_class = github3.auths.Authorization
    example_data = TestAuthorization.example_data.copy()

    def after_setup(self):
        """Disable authentication on the Session."""
        self.session.has_auth.return_value = False
        self.session.auth = None

    def test_add_scopes(self):
        """Test that adding scopes requires authentication."""
        self.assert_requires_auth(self.instance.add_scopes)

    def test_delete(self):
        """Test that deleteing an authorization requires authentication."""
        self.assert_requires_auth(self.instance.delete)

    def test_remove_scopes(self):
        """Test that removing scopes requires authentication."""
        self.assert_requires_auth(self.instance.remove_scopes)

    def test_replace_scopes(self):
        """Test that replacing scopes requires authentication."""
        self.assert_requires_auth(self.instance.replace_scopes)
