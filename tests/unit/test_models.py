import pytest

from datetime import datetime
from github3.models import GitHubCore, GitHubObject
from . import helper


class MyTestRefreshClass(GitHubCore):
    """Subclass for testing refresh on GitHubCore."""
    def __init__(self, example_data, session=None):
        super(MyTestRefreshClass, self).__init__(example_data, session)
        self._api = example_data['url']
        self.last_modified = example_data['last_modified']
        self.etag = example_data['etag']


class MyGetAttrTestClass(GitHubObject):
    """Subclass for testing getattr on GitHubObject."""

    def __init__(self, example_data, session=None):
        super(MyGetAttrTestClass, self).__init__(example_data)

    def _update_attributes(self, json_data):
        self.fake_attr = json_data.get('fake_attr')


class TestGitHubObject(helper.UnitHelper):
    """Test methods on GitHubObject class."""

    described_class = MyGetAttrTestClass
    example_data = {
        'fake_attr': 'foo',
        'another_fake_attr': 'bar'
    }

    def test_exposes_attributes(self):
        """Verify JSON attributes are exposed even if not explicitly set."""
        assert self.instance.another_fake_attr == 'bar'

    def test_missingattribute(self):
        """Test AttributeError is raised when attribute is not in JSON."""
        with pytest.raises(AttributeError):
            self.instance.missingattribute


class TestGitHubCore(helper.UnitHelper):

    described_class = MyTestRefreshClass
    last_modified = datetime.now().strftime(
        '%a, %d %b %Y %H:%M:%S GMT'
    )
    url = 'https://api.github.com/foo'
    etag = '644b5b0155e6404a9cc4bd9d8b1ae730'
    example_data = {
        'url': url,
        'last_modified': last_modified,
        'etag': etag
    }

    def test_refresh(self):
        """Verify the request of refreshing an object."""
        instance = self.instance.refresh()
        assert isinstance(instance, MyTestRefreshClass)
        expected_headers = None
        self.session.get.assert_called_once_with(
            self.url,
            headers=expected_headers,
        )

    def test_refresh_last_modified(self):
        """Verify the request of refreshing an object."""
        expected_headers = {
            'If-Modified-Since': self.last_modified
        }

        self.instance.refresh(conditional=True)

        self.session.get.assert_called_once_with(
            self.url,
            headers=expected_headers,
        )

    def test_refresh_etag(self):
        """Verify the request of refreshing an object."""
        self.instance.last_modified = None
        expected_headers = {
            'If-None-Match': self.etag
        }

        self.instance.refresh(conditional=True)

        self.session.get.assert_called_once_with(
            self.url,
            headers=expected_headers,
        )
