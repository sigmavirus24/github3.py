import github3
from github3.structs import GitHubIterator
from tests.utils import BaseCase, expect


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
        expect(i.headers.get('If-None-Match')) == '"foobarbogus"'

    def test_repr(self):
        expect(repr(self.i)) == '<GitHubIterator [{0}, /users]>'.format(
            self.num)

    def test_nexts(self):
        self.response('user', _iter=True)
        self.get(self.api_url)
        self.conf = {'params': None, 'headers': {}}
        self.j = GitHubIterator(self.num, self.api_url, github3.users.User,
                                self.g)
        expect(self.j.next().login) == next(self.i).login
        self.mock_assertions()

    def test_catch_etags(self):
        self.response('user', _iter=True, etag='"foobarbogus"')
        self.get(self.api_url)
        self.conf = {'params': None, 'headers': {}}

        expect(next(self.i)).isinstance(github3.users.User)
        expect(self.i.etag) == '"foobarbogus"'
        self.mock_assertions()

    def test_catch_None(self):
        self.response('', 200)
        self.get(self.api_url)
        self.conf = {'params': None, 'headers': {}}

        with expect.raises(StopIteration):
            next(self.i)

        self.mock_assertions()

    def test_entire_while_loop(self):
        self.response('user', _iter=True)
        self.get(self.api_url)
        self.conf = {'params': None, 'headers': {}}

        expect(next(self.i)).isinstance(github3.users.User)

        with expect.raises(StopIteration):
            next(self.i)

        self.mock_assertions()

    def test_count_reaches_0(self):
        self.response('user', _iter=True)
        self.get(self.api_url)
        self.conf = {'params': None, 'headers': {}}
        self.i = GitHubIterator(1, self.api_url, github3.users.User, self.g)

        expect(next(self.i)).isinstance(github3.users.User)
        with expect.raises(StopIteration):
            next(self.i)

        self.mock_assertions()
