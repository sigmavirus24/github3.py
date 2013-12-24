import github3

from .helper import IntegrationHelper


class TestAPI(IntegrationHelper):
    def get_client(self):
        return github3.gh

    def test_search_repositories(self):
        """Test the ability to use the repository search endpoint"""
        cassette_name = self.cassette_name('search_repositories',
                                           cls='GitHub')
        with self.recorder.use_cassette(cassette_name):
            repos = self.gh.search_repositories('github3 language:python')
            assert isinstance(next(repos),
                              github3.search.RepositorySearchResult)
