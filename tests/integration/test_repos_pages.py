import github3

from .helper import IntegrationHelper


class TestRepositoryPages(IntegrationHelper):
    def test_latest_pages_build(self):
        """Test the ability to retrieve the latest pages build for a repo."""
        self.token_login()
        cassette_name = self.cassette_name('latest_pages_build')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            assert repository is not None
            latest_build = repository.latest_pages_build()

        assert isinstance(latest_build, github3.repos.pages.PagesBuild)

    def test_pages(self):
        """
        Test the ability to retrieve information about a repository's pages.
        """
        self.token_login()
        cassette_name = self.cassette_name('pages')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            assert repository is not None
            pages_info = repository.pages()

        assert isinstance(pages_info, github3.repos.pages.PagesInfo)

    def test_pages_builds(self):
        """Test the ability to list the pages builds."""
        self.token_login()
        cassette_name = self.cassette_name('pages_builds')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'delete_contents')
            assert repository is not None
            for build in repository.pages_builds():
                assert isinstance(build, github3.repos.pages.PagesBuild)
