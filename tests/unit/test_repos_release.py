from github3.repos.release import Release, Asset

from .helper import (UnitHelper, UnitIteratorHelper, create_url_helper, mock,
                    create_example_data_helper)

import json
import pytest

url_for = create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/releases'
)


class TestRelease(UnitHelper):
    described_class = Release
    get_release_example_data = create_example_data_helper('repos_release_example')
    example_data = get_release_example_data()

    # Attribute tests
    def test_original_assets(self):
        assert self.instance.original_assets is not None
        assert isinstance(self.instance.original_assets[0], Asset)

    def test_has_upload_urlt(self):
        assert self.instance.upload_urlt is not None

    # Method tests
    def test_tarball_archive(self):
        """Verify that we generate the correct URL for a tarball archive."""
        self.instance.archive(format='tarball')

        self.session.get.assert_called_once_with(
            'https://api.github.com/repos/octocat/Hello-World/tarball/v1.0.0',
            allow_redirects=True,
            stream=True
        )

    def test_zipball_archive(self):
        """Verify that we generate the correct URL for a zipball archive."""
        self.instance.archive(format='zipball')

        self.session.get.assert_called_once_with(
            'https://api.github.com/repos/octocat/Hello-World/zipball/v1.0.0',
            allow_redirects=True,
            stream=True
        )

    def test_unsupported_archive(self):
        """Do not make a request if the archive format is unsupported."""
        self.instance.archive(format='clearly fake')

        assert self.session.get.called is False

    def test_delete(self):
        self.instance.delete()
        self.session.delete.assert_called_once_with(
            self.example_data['url'],
            headers={'Accept': 'application/vnd.github.manifold-preview'}
        )

    def test_upload_asset(self):
        self.session.post.return_value = mock.Mock(
            status_code=201, json=lambda: self.example_data["assets"][0])
        with open(__file__) as fd:
            content = fd.read()
            self.instance.upload_asset(
                'text/plain', 'test_repos_release.py', content,
            )
            self.post_called_with(
                url_for('/1/assets?name=%s' % 'test_repos_release.py'),
                data=content,
                headers=None
            )

    def test_upload_asset_with_a_label(self):
        self.session.post.return_value = mock.Mock(
            status_code=201, json=lambda: self.example_data["assets"][0])
        with open(__file__) as fd:
            content = fd.read()
            self.instance.upload_asset(
                'text/plain', 'test_repos_release.py', content, 'test-label'
            )
            self.post_called_with(
                url_for('/1/assets?name=%s&label=%s' % (
                    'test_repos_release.py', 'test-label')),
                data=content,
                headers=None
            )


class TestReleaseIterators(UnitIteratorHelper):

    """Test iterator methods on the Release class."""

    described_class = Release
    example_data = TestRelease.example_data.copy()

    def test_assets(self):
        """Test the request to retrieve a release's assets."""
        i = self.instance.assets()
        self.get_next(i)

        self.session.get.assert_called_once_with(
            url_for('1/assets'),
            params={'per_page': 100},
            headers={}
        )


class TestAsset(UnitHelper):
    described_class = Asset
    get_asset_example_data = create_example_data_helper('repos_asset_example')
    example_data = get_asset_example_data()

    def test_delete(self):
        """Verify the request to delete an Asset."""
        self.instance.delete()

        self.session.delete.assert_called_once_with(
            url_for('/assets/1'),
            headers=Release.CUSTOM_HEADERS
        )

    @pytest.mark.xfail
    def test_download(self):
        """Verify the request to download an Asset file."""
        with mock.patch('github3.utils.stream_response_to_file') as stream:
            self.instance.download()

        self.session.get.assert_called_once_with(
            url_for('/assets/1'),
            stream=True,
            allow_redirects=False,
            headers={'Accept': 'application/octect-stream'}
        )
        assert stream.called is False

    def test_edit_without_label(self):
        self.instance.edit('new name')
        self.session.patch.assert_called_once_with(
            self.example_data['url'],
            data='{"name": "new name"}',
            headers={'Accept': 'application/vnd.github.manifold-preview'}
        )

    def test_edit_with_label(self):
        self.instance.edit('new name', 'label')
        headers = {'Accept': 'application/vnd.github.manifold-preview'}
        _, args, kwargs = list(self.session.patch.mock_calls[0])
        assert self.example_data['url'] in args
        assert kwargs['headers'] == headers
        assert json.loads(kwargs['data']) == {
            'name': 'new name', 'label': 'label'
            }
