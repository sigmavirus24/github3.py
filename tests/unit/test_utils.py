from datetime import datetime
from github3.utils import stream_response_to_file, timestamp_parameter

import io
import mock
import pytest
import requests


class TestTimestampConverter:
    def test_datetimes(self):
        timestamp = datetime(2010, 6, 1, 12, 15, 30)
        assert '2010-06-01T12:15:30Z' == timestamp_parameter(timestamp)

    def test_valid_datestring(self):
        testvals = (
            '2010-06-01',
            '2010-06-01T12:15:30',
            '2010-06-01T12:14:30.12321+02:00',
            '2010-06-01T12:14:30.12321-02:00',
            '2010-06-01T12:14:30.2115Z',
        )
        for timestamp in testvals:
            assert timestamp == timestamp_parameter(timestamp)

    def test_invalid_datestring(self):
        testvals = (
            '2012-16-04',
            '2012-06-01v!',
            'fish',
            '2010-06-01T12:14:30.12321+02',
            '2010-06-01T12:70:30.12321+02',
        )
        for timestamp in testvals:
            pytest.raises(ValueError, timestamp_parameter, timestamp)

    def test_none_handling(self):
        assert timestamp_parameter(None, allow_none=True) is None
        pytest.raises(ValueError, timestamp_parameter, None,
                      allow_none=False)

    def test_invalid_type_handling(self):
        pytest.raises(ValueError, timestamp_parameter, 1)


@pytest.fixture
def mocked_open():
    return mock.mock_open()


@pytest.fixture
def response():
    r = requests.Response()
    r.raw = io.BytesIO(b'fake data')
    r.headers.update({'content-disposition': 'filename=a_file_name'})
    return r


class OpenFile:
    def __init__(self):
        self.data = b''
        self.written_to = False

    def write(self, data):
        self.written_to = True
        self.data += data


class TestStreamingDownloads:
    def test_opens_a_new_file(self, mocked_open, response):
        with mock.patch('github3.utils.open', mocked_open, create=True):
            stream_response_to_file(response, 'some_file')

        mocked_open.assert_called_once_with('some_file', 'wb')
        mocked_open().write.assert_called_once_with(b'fake data')
        mocked_open().close.assert_called_once_with()

    def test_uses_existing_file(self, response):
        fd = OpenFile()
        stream_response_to_file(response, fd)
        assert fd.written_to is True
        assert fd.data == b'fake data'

    def test_finds_filename_in_headers(self, mocked_open, response):
        with mock.patch('github3.utils.open', mocked_open, create=True):
            stream_response_to_file(response)

        mocked_open.assert_called_once_with('a_file_name', 'wb')
        mocked_open().write.assert_called_once_with(b'fake data')
        mocked_open().close.assert_called_once_with()
