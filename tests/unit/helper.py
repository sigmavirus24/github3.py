import mock
import requests
import unittest

MockedSession = mock.create_autospec(requests.Session)


class UnitHelper(unittest.TestCase):
    # Sub-classes must assign the class to this during definition
    described_class = None
    # Sub-classes must also assign a dictionary to this during definition
    example_data = {}

    def create_session_mock(self, *args):
        session = MockedSession()
        base_attrs = ['headers', 'auth']
        attrs = dict(
            (key, mock.Mock()) for key in set(args).union(base_attrs)
        )
        session.configure_mock(**attrs)
        return session

    def setUp(self):
        self.session = self.create_session_mock()
        self.instance = self.described_class(self.example_data, self.session)
