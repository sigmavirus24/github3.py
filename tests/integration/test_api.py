import github3

from .helper import IntegrationHelper


class TestAPI(IntegrationHelper):
    def get_client(self):
        return github3.api.gh

    def test_emojis(self):
        """Test the ability to use the /emojis endpoint"""
        cassette_name = self.cassette_name('emojis', cls='GitHub')
        with self.recorder.use_cassette(cassette_name):
            emojis = self.gh.emojis()

        assert emojis['+1'] is not None

    def test_search_code(self):
        """Test the ability to use the code search endpoint"""
        cassette_name = self.cassette_name('search_code',
                                           cls='GitHub')
        with self.recorder.use_cassette(cassette_name):
            repos = self.gh.search_code(
                'HTTPAdapter in:file language:python'
                ' repo:kennethreitz/requests'
                )
            assert isinstance(next(repos),
                              github3.search.CodeSearchResult)

    def test_search_users(self):
        """Test the ability to use the user search endpoint"""
        cassette_name = self.cassette_name('search_users', cls='GitHub')
        with self.recorder.use_cassette(cassette_name):
            users = self.gh.search_users('tom followers:>1000')
            assert isinstance(next(users),
                              github3.search.UserSearchResult)

    def test_search_issues(self):
        """Test the ability to use the issues search endpoint"""
        cassette_name = self.cassette_name('search_issues',
                                           cls='GitHub')
        with self.recorder.use_cassette(cassette_name):
            issues = self.gh.search_issues('github3 label:Bug')
            assert isinstance(next(issues),
                              github3.search.IssueSearchResult)

    def test_search_repositories(self):
        """Test the ability to use the repository search endpoint"""
        cassette_name = self.cassette_name('search_repositories',
                                           cls='GitHub')
        with self.recorder.use_cassette(cassette_name):
            repos = self.gh.search_repositories('github3 language:python')
            assert isinstance(next(repos),
                              github3.search.RepositorySearchResult)
