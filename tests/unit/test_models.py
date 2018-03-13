import io
import json
import pytest
import requests

from datetime import datetime, timedelta
from github3 import exceptions, GitHubError
from github3.models import GitHubCore
from unittest import TestCase
from . import helper


class MyTestRefreshClass(GitHubCore):
    """Subclass for testing refresh on GitHubCore."""
    def __init__(self, example_data, session):
        super(MyTestRefreshClass, self).__init__(example_data, session)
        self._api = example_data['url']
        self.last_modified = example_data['last_modified']
        self.etag = example_data['etag']


class TestGitHubError(TestCase):
    """Test methods on GitHubError class."""

    def setUp(self):
        response = requests.Response()
        response.status_code = 400
        message = b'{"message": "m", "errors": ["e"]}'
        response.raw = io.BytesIO(message)
        self.instance = GitHubError(response)

    def test_message_is_empty(self):
        """Verify instance message is correct."""
        response = requests.Response()
        response.status_code = 400
        response.raw = io.BytesIO()
        error = GitHubError(response)
        assert error.message == '[No message]'

    def test_message(self):
        """Verify instance message is correct."""
        assert self.instance.msg == self.instance.message

    def test_str(self):
        """Verify instance string is formatted correctly."""
        assert str(self.instance) == '400 m'


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
        'etag': etag,
        'fake_attr': 'foo',
    }

    def test_boolean(self):
        """Verify boolean tests for response codes correctly."""
        response = requests.Response()
        response.status_code = 200
        boolean = self.instance._boolean(response=response,
                                         true_code=200,
                                         false_code=204)

        assert boolean is True

    def test_boolean_raises_exception(self):
        """Verify boolean tests for response codes correctly."""
        response = requests.Response()
        response.status_code = 512
        response.raw = io.BytesIO()
        with pytest.raises(exceptions.GitHubError):
            self.instance._boolean(response=response,
                                   true_code=200,
                                   false_code=204)

    def test_boolean_false_code(self):
        """Verify boolean tests for response codes correctly."""
        response = requests.Response()
        response.status_code = 204
        boolean = self.instance._boolean(response=response,
                                         true_code=200,
                                         false_code=204)

        assert boolean is False

    def test_boolean_empty_response(self):
        """Verify boolean tests for response codes correctly."""
        boolean = self.instance._boolean(response=None,
                                         true_code=200,
                                         false_code=204)

        assert boolean is False

    def test_exposes_attributes(self):
        """Verify JSON attributes are exposed even if not explicitly set."""
        assert self.instance.fake_attr == 'foo'

    def test_from_json(self):
        """Verify that method returns GitHubObject from json."""
        github_core = GitHubCore.from_json('{}', self.session)
        assert isinstance(github_core, GitHubCore)

    def test_instance_or_null(self):
        """Verify method raises exception when json is not a dict."""
        with pytest.raises(exceptions.UnprocessableResponseBody):
            self.instance._instance_or_null(GitHubCore, [])

    def test_json(self):
        """Verify JSON information is retrieved correctly."""
        response = requests.Response()
        response.headers['Last-Modified'] = 'foo'
        response.headers['ETag'] = 'bar'
        response.raw = io.BytesIO(b'{}')
        response.status_code = 200

        json = self.instance._json(response, 200)
        assert json['Last-Modified'] == 'foo'
        assert json['ETag'] == 'bar'

    def test_json_status_code_does_not_match(self):
        """Verify JSON information is retrieved correctly."""
        response = requests.Response()
        response.status_code = 204

        with pytest.raises(exceptions.UnexpectedResponse):
            self.instance._json(response, 200)

    def test_missingattribute(self):
        """Test AttributeError is raised when attribute is not in JSON."""
        with pytest.raises(AttributeError):
            self.instance.missingattribute

    def test_refresh(self):
        """Verify the request of refreshing an object."""
        instance = self.instance.refresh()
        assert isinstance(instance, MyTestRefreshClass)
        expected_headers = None
        self.session.get.assert_called_once_with(
            self.url,
            headers=expected_headers,
        )

    def test_refresh_custom_headers(self):
        """Verify the request of refreshing an object."""
        self.instance.CUSTOM_HEADERS = {
            'Accept': 'application/vnd.github.drax-preview+json'
        }
        expected_headers = {
            'Accept': 'application/vnd.github.drax-preview+json'
        }

        self.instance.refresh()

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

    def test_refresh_json(self):
        """Verify refreshing an object updates stored json data."""
        expected_data = {
            'changed_files': 4
        }
        response = requests.Response()
        response.status_code = 200
        response.raw = io.BytesIO(json.dumps(expected_data).encode('utf8'))
        self.session.get.return_value = response

        self.instance.refresh()

        assert 'changed_files' in self.instance.as_dict()
        assert self.instance.changed_files == 4

    def test_strptime(self):
        """Verify that method converts ISO 8601 formatted string."""
        dt = self.instance._strptime('2015-06-18T19:53:04Z')
        assert dt.tzname() == 'UTC'
        assert dt.dst() == timedelta(0)
        assert dt.utcoffset() == timedelta(0)

    def test_strptime_time_str_required(self):
        """Verify that method converts ISO 8601 formatted string."""
        assert self.instance._strptime('') is None


class TestGitHubCoreIssue672(helper.UnitHelper):

    described_class = MyTestRefreshClass
    last_modified = datetime.now().strftime(
        '%a, %d %b %Y %H:%M:%S GMT'
    )
    url = 'https://api.github.com/foo?bar=1'
    etag = '644b5b0155e6404a9cc4bd9d8b1ae730'
    example_data = {
        'url': url,
        'last_modified': last_modified,
        'etag': etag,
        'fake_attr': 'foo',
    }

    def test_issue_672(self):
        """Verify that _api property contains URL query"""
        assert '?' in self.instance._api
        assert self.instance._api == self.url
