"""Integration tests for Tree."""
import github3
from .helper import IntegrationHelper


class TestTree(IntegrationHelper):

    """Integration tests for methods on the Test class."""

    def test_recurse(self):
        """Test recurse on tree"""
        cassette_name = self.cassette_name('recurse')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            t = repository.tree('75b347329e3fc87ac78895ca1be58daff78872a1').recurse()
            assert isinstance(t.tree[0], github3.git.Hash)
            assert repr(t.tree[0]).startswith('<Hash')
