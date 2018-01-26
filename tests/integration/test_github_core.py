from .helper import IntegrationHelper


class TestGitHubCore(IntegrationHelper):
    def test_ratelimit_remaining(self):
        cassette_name = self.cassette_name('ratelimit_remaining')
        with self.recorder.use_cassette(cassette_name):
            assert self.gh.ratelimit_remaining > 0

    def test_ratelimit_remaining_search(self):
        """Test if search iterators return search ratelimit"""

        def _get_ratelimit(resource):
            resources = self.gh.rate_limit().get('resources', {})
            rate_limit = resources.get(resource, {})
            return rate_limit.get('remaining', -1)

        cassette_name = self.cassette_name('ratelimit_remaining_search')

        # Run cassette to get correct remaining rate limit from responses.
        with self.recorder.use_cassette(cassette_name):
            correct_ratelimit_search = _get_ratelimit('search')
            correct_ratelimit_core = _get_ratelimit('core')

        # Re-run cassette to test functions under test.
        with self.recorder.use_cassette(cassette_name):
            result_iterator = self.gh.search_code(
                'HTTPAdapter in:file language:python'
                ' repo:kennethreitz/requests'
                )
            ratelimit_remaining_search = result_iterator.ratelimit_remaining
            ratelimit_remaining_core = self.gh.ratelimit_remaining

            assert ratelimit_remaining_search != ratelimit_remaining_core
            assert ratelimit_remaining_core == correct_ratelimit_core
            assert ratelimit_remaining_search == correct_ratelimit_search
