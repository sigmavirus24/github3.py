from .helper import IntegrationHelper


class TestGitHubIterator(IntegrationHelper):
    def test_resets_etag(self):
        cassette_name = self.cassette_name('resets_etag')
        with self.recorder.use_cassette(cassette_name):
            users_iter = self.gh.iter_all_users(number=10)
            assert users_iter.etag is None
            next(users_iter)  # Make the request
            assert users_iter.etag is not None
            users_iter.refresh()
            assert users_iter.etag is None
