from .helper import UnitHelper
from github3.structs import GitHubIterator


class TestGitHubIterator(UnitHelper):
    described_class = GitHubIterator
    example_data = None

    def setUp(self):
        self.session = self.create_mocked_session()
        self.url = 'https://api.github.com/users'
        self.count = -1
        self.cls = object

    def test_stores_headers_properly(self):
        headers = {'Accept': 'foo'}
        session, url, count, cls = self.session, self.url, self.count, self.cls
        i = GitHubIterator(count, url, cls, session, headers=headers)
        assert i.headers != {}
        assert i.headers.get('Accept') == 'foo'
