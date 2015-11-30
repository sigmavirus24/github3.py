import github3
import os
import tempfile

from .helper import IntegrationHelper


class TestRelease(IntegrationHelper):
    def test_archive(self):
        """Test the ability to download a release archive."""
        cassette_name = self.cassette_name('archive')
        with self.recorder.use_cassette(cassette_name,
                                        preserve_exact_body_bytes=True):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            release = repository.release(76677)
            _, filename = tempfile.mkstemp()
            release.archive('tarball', path=filename)

        with open(filename, 'rb') as fd:
            assert len(fd.read(1024)) > 0

        os.unlink(filename)

    def test_asset(self):
        """Test the ability to retrieve a single asset from a release."""
        cassette_name = self.cassette_name('asset')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            release = repository.release(76677)
            asset = release.asset(37944)

        assert asset is not None
        assert isinstance(asset, github3.repos.release.Asset)

    def test_assets(self):
        """Test the ability to iterate over the assets of a release."""
        cassette_name = self.cassette_name('assets')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            release = repository.release(76677)
            for asset in release.assets():
                assert isinstance(asset, github3.repos.release.Asset)
            assert asset is not None

    def test_delete(self):
        """Test the ability to delete a release."""
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
                    'text/plain', 'test_repos_release.py', fd.read(),
                )
            assert isinstance(asset, github3.repos.release.Asset)
            release.delete()

    def test_upload_asset_with_a_label(self):
        """Test the ability to upload an asset to a release with a label."""
        self.token_login()
        cassette_name = self.cassette_name('upload_asset_with_a_label')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'github3.py')
            release = repository.create_release(
                '0.8.0.pre', 'develop', '0.8.0.pre fake release with upload',
                'To be deleted'
                )
            with open(__file__) as fd:
                asset = release.upload_asset(
                    'text/plain', 'test_repos_release.py', fd.read(),
                    'test-label',
                )
            release.delete()
        assert isinstance(asset, github3.repos.release.Asset)


class TestAsset(IntegrationHelper):
    def test_delete(self):
        """Test the ability to delete an asset."""
        self.basic_login()
        cassette_name = self.cassette_name('delete')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('github3py', 'github3.py')
            release = repository.release(833407)
            asset = release.asset(370020)
            assert asset.delete() is True

    def test_download(self):
        """Test the ability to download an asset."""
        cassette_name = self.cassette_name('download')
        with self.recorder.use_cassette(cassette_name,
                                        preserve_exact_body_bytes=True):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            release = repository.release(76677)
            asset = next(release.assets())
            _, filename = tempfile.mkstemp()
            asset.download(filename)

        with open(filename, 'rb') as fd:
            assert len(fd.read(1024)) > 0

        os.unlink(filename)

    def test_download_when_authenticated(self):
        """Test the ability to download an asset when authenticated."""
        self.basic_login()
        cassette_name = self.cassette_name('download_when_authenticated')
        with self.recorder.use_cassette(cassette_name,
                                        preserve_exact_body_bytes=True):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            release = repository.release(76677)
            asset = next(release.assets())
            _, filename = tempfile.mkstemp()
            assert asset.session.auth is not None
            asset.download(filename)
            assert asset.session.auth is not None

        with open(filename, 'rb') as fd:
            assert len(fd.read(1024)) > 0

        os.unlink(filename)

    def test_edit(self):
        """Test the ability to edit an existing asset."""
        self.basic_login()
        cassette_name = self.cassette_name('edit')
        with self.recorder.use_cassette(cassette_name,
                                        preserve_exact_body_bytes=True):
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
            assert asset.edit('A new name for this asset') is True
            release.delete()
