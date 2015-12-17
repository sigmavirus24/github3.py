import github3
import pytest
import mock
from .helper import create_example_data_helper

get_user_key_example_data = create_example_data_helper('user_key_example')


class TestGitHubObject:
    """Test methods on GitHubObject class."""

    def test_getattr(self):
        """Test access to JSON data if attribute is not explicitly set."""

        key = github3.users.Key(get_user_key_example_data())
        # verified attribute is not set in _update_attributes for Key class
        with pytest.raises(KeyError):
            key.__dict__['verified']

        assert key.verified is True

    def test_getattr_attribute_not_in_json(self):
        """Test AttributeError is raised when attribute is not in JSON."""
        key = github3.users.Key(get_user_key_example_data())
        with pytest.raises(AttributeError):
            key.fakeattribute

    @mock.patch('github3.models.GitHubObject.__getattr__')
    def test_getattr_called(self, mocked_getattr):
        """Show that getattr is called if attribute does not exist."""
        key = github3.users.Key(get_user_key_example_data())
        key.fakeattribute

        assert mocked_getattr.called is True

    @mock.patch('github3.models.GitHubObject.__getattr__')
    def test_getattr_not_called_on_base_class(self, mocked_getattr):
        """Show getattr is not called if attribute exists on base class."""
        key = github3.users.Key(get_user_key_example_data())
        key._uniq
        assert mocked_getattr.called is False
