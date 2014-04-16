import github3

from .helper import IntegrationHelper


class TestRepositoryPages(IntegrationHelper):
    def test_iter_pages_builds(self):
        """Test the ability to list the pages builds."""
        self.basic_login()
        cassette_name = self.cassette_name('pages_builds')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            assert repository is not None
            for build in repository.iter_pages_builds():
                assert isinstance(build, github3.repos.pages.PagesBuild)
