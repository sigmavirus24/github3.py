from github3.repos.release import Release, Asset

from .helper import UnitHelper, UnitIteratorHelper, create_url_helper, mock

import json
import pytest

url_for = create_url_helper(
    'https://api.github.com/repos/octocat/Hello-World/releases'
)


class TestRelease(UnitHelper):
    described_class = Release
    example_data = {
        "url": url_for("/1"),
        "html_url": "https://github.com/octocat/Hello-World/releases/v1.0.0",
        "assets": [{
            "url": url_for("/assets/1"),
            "id": 1,
            "name": "example.zip",
            "label": "short description",
            "state": "uploaded",
            "content_type": "application/zip",
            "size": 1024,
            "download_count": 42,
            "created_at": "2013-02-27T19:35:32Z",
            "updated_at": "2013-02-27T19:35:32Z"
            }],
        "assets_url": url_for("/1/assets"),
        "upload_url": url_for("/1/assets{?name}"),
        "id": 1,
        "tag_name": "v1.0.0",
        "target_commitish": "master",
        "name": "v1.0.0",
        "body": "Description of the release",
        "draft": False,
        "prerelease": False,
        "created_at": "2013-02-27T19:35:32Z",
        "published_at": "2013-02-27T19:35:32Z"
        }

    # Attribute tests
    def test_original_assets(self):
        assert self.instance.original_assets is not None
        assert isinstance(self.instance.original_assets[0], Asset)

    def test_has_upload_urlt(self):
        assert self.instance.upload_urlt is not None

    # Method tests
    def test_delete(self):
        self.instance.delete()
        self.session.delete.assert_called_once_with(
            self.example_data['url'],
            headers={'Accept': 'application/vnd.github.manifold-preview'}
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
    example_data = {
        "url": url_for("/assets/1"),
        "id": 1,
        "name": "example.zip",
        "label": "short description",
        "state": "uploaded",
        "content_type": "application/zip",
        "size": 1024,
        "download_count": 42,
        "created_at": "2013-02-27T19:35:32Z",
        "updated_at": "2013-02-27T19:35:32Z"
        }

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
