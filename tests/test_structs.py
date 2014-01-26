import github3
from github3.structs import GitHubIterator
from tests.utils import BaseCase
from mock import patch


class TestGitHubIterator(BaseCase):
    def setUp(self):
        super(TestGitHubIterator, self).setUp()
        self.api_url = 'https://api.github.com/users'
        self.num = 10
        self.i = GitHubIterator(self.num, self.api_url, github3.users.User,
                                self.g)

    def test_headers(self):
        i = GitHubIterator(self.i.count, self.i.url, self.i.cls, self.g,
                           etag='"foobarbogus"')
        assert i.headers.get('If-None-Match') == '"foobarbogus"'

    def test_repr(self):
        assert repr(self.i) == '<GitHubIterator [{0}, /users]>'.format(
            self.num)

    def test_nexts(self):
        self.response('user', _iter=True)
        self.get(self.api_url)
        self.conf = {'params': {'per_page': 10}, 'headers': {}}
        self.j = GitHubIterator(self.num, self.api_url, github3.users.User,
                                self.g)
        assert self.j.next().login == next(self.i).login
        self.mock_assertions()

    def test_catch_etags(self):
        self.response('user', _iter=True, etag='"foobarbogus"')
        self.get(self.api_url)
        self.conf = {'params': {'per_page': 10}, 'headers': {}}

        assert isinstance(next(self.i), github3.users.User)
        assert self.i.etag == '"foobarbogus"'
        self.mock_assertions()

    def test_catch_None(self):
        self.response('', 200)
        self.get(self.api_url)
        self.conf = {'params': {'per_page': 10}, 'headers': {}}

        self.assertRaises(StopIteration, next, self.i)

        self.mock_assertions()

    def test_entire_while_loop(self):
        self.response('user', _iter=True)
        self.get(self.api_url)
        self.conf = {'params': {'per_page': 10}, 'headers': {}}

        assert isinstance(next(self.i), github3.users.User)

        self.assertRaises(StopIteration, next, self.i)

        self.mock_assertions()

    def test_count_reaches_0(self):
        self.response('user', _iter=True)
        self.get(self.api_url)
        self.conf = {'params': {'per_page': 1}, 'headers': {}}
        self.i = GitHubIterator(1, self.api_url, github3.users.User, self.g)

        assert isinstance(next(self.i), github3.users.User)
        self.assertRaises(StopIteration, next, self.i)

        self.mock_assertions()

    def test_refresh(self):
        with patch.object(GitHubIterator, '__iter__') as i:
            self.i.refresh()
            i.__iter__.assert_called()

            i.reset_mock()
            self.i.refresh(True)
            i.__iter__.assert_called()
