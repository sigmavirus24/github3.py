"""Integration tests for Git."""
import github3
from .helper import IntegrationHelper


class TestTree(IntegrationHelper):

    """Integration tests for methods on the Test class."""

    def test_inequality(self):
        """Test that a tree and its recursed tree are not equal."""
        cassette_name = self.cassette_name('ne')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            tree = repository.tree(
                '96726db07528a87b7c1f266ed42cd321070470c2'
            )
            recursed = tree.recurse()
            assert tree != recursed

    def test_recurse(self):
        """Test recurse on tree"""
        cassette_name = self.cassette_name('recurse')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            t = repository.tree(
                '75b347329e3fc87ac78895ca1be58daff78872a1'
            ).recurse()
            assert isinstance(t.tree[0], github3.git.Hash)
            assert repr(t.tree[0]).startswith('<Hash')


class TestReference(IntegrationHelper):

    """Integration tests for methods on the Reference class."""

    def test_update(self):
        """Show that user can update a reference."""
        self.token_login()
        cassette_name = self.cassette_name('update')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('itsmemattchung', 'github3.py')
            reference = repository.ref(
                'heads/migrate-tests/git-integration-test'
            )
            assert reference.update(
                'b8bcee4db99325949c4171590b8fbcc8354d54d8'
            ) is True
