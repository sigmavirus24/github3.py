"""Unit tests for the auths module."""
import github3

from .helper import UnitHelper, create_url_helper

url_for = create_url_helper('https://api.github.com/authorizations/1')


class TestAuthorization(UnitHelper):

    """Authorization unit tests."""

    described_class = github3.auths.Authorization
    example_data = {
        "id": 1,
        "url": "https://api.github.com/authorizations/1",
        "scopes": [
            "public_repo"
        ],
        "token": "abc123",
        "app": {
            "url": "http://my-github-app.com",
            "name": "my github app",
            "client_id": "abcde12345fghij67890"
        },
        "note": "optional note",
        "note_url": "http://optional/note/url",
        "updated_at": "2011-09-06T20:39:23Z",
        "created_at": "2011-09-06T17:26:27Z"
    }

    def test_add_scopes(self):
        """Test the request to add scopes to an authorization."""
        self.instance.add_scopes(['scope-one', 'scope-two'])

        self.post_called_with(url_for(''), data={
            'add_scopes': ['scope-one', 'scope-two'],
        })

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
