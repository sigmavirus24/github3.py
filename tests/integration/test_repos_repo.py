import github3

from .helper import IntegrationHelper


class TestRepository(IntegrationHelper):
    def test_create_release(self):
        """Test the ability to create a release on a repository."""
        self.token_login()
        cassette_name = self.cassette_name('create_release')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'charade')
            assert repository is not None
            release = repository.create_release(
                '1.0.3.test', 'f1d4e150be7070adfbbdca164328d69723e096ec',
                'Test release'
                )

        assert isinstance(release, github3.repos.release.Release)

    def test_iter_languages(self):
        """Test that a repository's languages can be retrieved."""
        cassette_name = self.cassette_name('iter_languages')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            for l in repository.iter_languages():
                assert 'ETag' not in l
                assert 'Last-Modified' not in l
                assert isinstance(l, tuple)

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
