from .helper import IntegrationHelper


class TestRelease(IntegrationHelper):
    def test_delete(self):
        """Test the ability to delete a release"""
        self.token_login()
        cassette_name = self.cassette_name('delete')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'github3.py')
            release = repository.create_release(
                '0.8.0.pre', 'develop', '0.8.0 fake release',
                'To be deleted'
                )
            assert release is not None
            assert release.delete() is True

    def test_edit(self):
        """Test the ability to edit a release on a repository."""
        self.token_login()
        cassette_name = self.cassette_name('edit')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'charade')
            release = repository.release(85783)
            assert release.edit(body='Test editing a release') is True
            assert release.body == 'Test editing a release'

    def test_upload_asset(self):
        """Test the ability to upload an asset to a release."""
        self.token_login()
        cassette_name = self.cassette_name('upload_asset')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'github3.py')
            release = repository.create_release(
                '0.8.0.pre', 'develop', '0.8.0 fake release with upload',
                'To be deleted'
                )
            with open(__file__) as fd:
                asset = release.upload_asset(
                    'text/plain', 'test_repos_release.py', fd.read()
                    )
            assert isinstance(asset, github3.repos.release.Asset)
            release.delete()
