from .helper import IntegrationHelper


class TestGitHubCore(IntegrationHelper):
    def test_ratelimit_remaining(self):
        cassette_name = self.cassette_name('ratelimit_remaining')
        with self.recorder.use_cassette(cassette_name):
            assert self.gh.ratelimit_remaining > 0
