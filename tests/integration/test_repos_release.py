from .helper import IntegrationHelper


class TestRelease(IntegrationHelper):
    def test_edit_release(self):
        """Test the ability to edit a release on a repository."""
        self.token_login()
        cassette_name = self.cassette_name('edit')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'charade')
            release = repository.release(85783)
            assert release.edit(body='Test editing a release') is True
            assert release.body == 'Test editing a release'
