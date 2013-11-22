import mock
import github3
import unittest

MockedSession = mock.create_autospec(github3.session.GitHubSession)


def build_url(self, *args, **kwargs):
    # We want to assert what is happening with the actual calls to the
    # Internet. We can proxy this.
    return github3.session.GitHubSession().build_url(*args, **kwargs)


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
        session.delete.return_value = None
        session.get.return_value = None
        session.patch.return_value = None
        session.post.return_value = None
        session.put.return_value = None
        return session

    def setUp(self):
        self.session = self.create_session_mock()
        self.instance = self.described_class(self.example_data, self.session)
        # Proxy the build_url method to the class so it can build the URL and
        # we can assert things about the call that will be attempted to the
        # internet
        self.described_class._build_url = build_url
