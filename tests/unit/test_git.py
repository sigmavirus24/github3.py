import github3

from .helper import (UnitHelper, create_example_data_helper, create_url_helper)

get_example_data = create_example_data_helper('tree_example')
url_for = create_url_helper('https://api.github.com/repos/octocat/Hello-World/'
                            'trees/9fb037999f264ba9a7fc6274d15fa3ae2ab98312')

delete_url_for = create_url_helper('https://api.github.com/repos/octocat/Hello-World/'
                                   'git/refs/heads/featureA')

get_commit_example_data = create_example_data_helper('commit_example')
get_reference_example_data = create_example_data_helper('reference_example')


class TestTree(UnitHelper):
    """Tree unit test"""

    described_class = github3.git.Tree
    example_data = get_example_data()

    def test_repr(self):
        """Assert Tree in in the repr."""
        assert isinstance(self.instance, github3.git.Tree)
        assert repr(self.instance).startswith('<Tree')

    def test_recurse(self):
        """Assert that URL is called"""
        self.instance.recurse()
        self.session.get.assert_called_once_with(
            url_for(),
            params={'recursive': '1'}
        )


class TestCommit(UnitHelper):

    "Commit unit test."""

    described_class = github3.git.Commit
    example_data = get_commit_example_data()

    def test_repr(self):
        assert repr(self.instance).startswith('<Commit')

    def test_committer_as_User(self):
        """Show that commit_as_User() returns instance of User."""
        user = self.instance.committer_as_User()
        assert isinstance(user, github3.users.User)

    def test_author_as_User(self):
        """Show that commit_as_Author() returns instance of User."""
        user = self.instance.author_as_User()
        assert isinstance(user, github3.users.User)


class TestReference(UnitHelper):

    """Reference unit test."""

    described_class = github3.git.Reference
    example_data = get_reference_example_data()

    def test_delete(self):
        self.instance.delete()
        self.session.delete.assert_called_once_with(
            delete_url_for()
        )

    def test_repr(self):
        assert repr(self.instance).startswith('<Reference')
        assert repr(self.instance.object).startswith('<Git Object')

    def test_update(self):
        """Show that a user can update the reference."""

        self.instance.update('fakesha', True)
        self.session.patch.assert_called_once_with(
            delete_url_for(),
            data='{"sha": "fakesha", "force": true}'
        )
