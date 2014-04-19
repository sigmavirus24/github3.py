from datetime import datetime
from github3.utils import timestamp_parameter

import pytest


class TestTimestampConverter:
    def test_datetimes(self):
        timestamp = datetime(2010, 6, 1, 12, 15, 30)
        assert '2010-06-01T12:15:30' == timestamp_parameter(timestamp)

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
