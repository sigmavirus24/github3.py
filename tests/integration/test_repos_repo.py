import github3

from .helper import IntegrationHelper


class TestRepository(IntegrationHelper):
    def test_iter_releases(self):
        """Test the ability to iterate over releases on a repository."""
        cassette_name = self.cassette_name('iter_releases')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            for release in repository.iter_releases():
                assert isinstance(release, github3.repos.release.Release)

    def test_release(self):
        """Test the ability to retrieve a single release."""
        cassette_name = self.cassette_name('release')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            release = repository.release(76677)
        assert isinstance(release, github3.repos.release.Release)
