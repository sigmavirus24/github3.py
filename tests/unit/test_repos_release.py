from github3.repos.release import Release, Asset

from .helper import UnitHelper

import json


def releases_url(path=''):
    url = "https://api.github.com/repos/octocat/Hello-World/releases"
    return url + path


class TestRelease(UnitHelper):
    described_class = Release
    example_data = {
        "url": releases_url("/1"),
        "html_url": "https://github.com/octocat/Hello-World/releases/v1.0.0",
        "assets": [{
            "url": releases_url("/assets/1"),
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
        "assets_url": releases_url("/1/assets"),
        "upload_url": releases_url("/1/assets{?name}"),
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
    def test_assets(self):
        assert self.instance.assets is not None
        assert isinstance(self.instance.assets[0], Asset)

    def test_has_upload_urlt(self):
        assert self.instance.upload_urlt is not None

    # Method tests
    def test_delete(self):
        self.instance.delete()
        self.session.delete.assert_called_once_with(
            self.example_data['url'],
            headers={'Accept': 'application/vnd.github.manifold-preview'}
        )


class TestAsset(UnitHelper):
    described_class = Asset
    example_data = {
        "url": releases_url("/assets/1"),
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
