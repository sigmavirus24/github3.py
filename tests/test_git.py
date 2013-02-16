import github3
from tests.utils import (expect, BaseCase, load)


class TestCommit(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestCommit, self).__init__(methodName)
        self.commit = github3.git.Commit(load('commit'))

    def test_repr(self):
        expect(repr(self.commit).startswith('<Commit'))

    def test_author_as_User(self):
        u = self.commit.author_as_User()
        expect(u).isinstance(github3.users.User)

    def test_committer_as_User(self):
        u = self.commit.committer_as_User()
        expect(u).isinstance(github3.users.User)


class TestReference(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestReference, self).__init__(methodName)
        self.ref = github3.git.Reference(load('ref'))
        self.api = ('https://api.github.com/repos/sigmavirus24/github3.py/'
                    'git/refs/heads/master')

    def setUp(self):
        super(TestReference, self).setUp()
        self.ref = github3.git.Reference(self.ref.to_json(), self.g)

    def test_repr(self):
        expect(repr(self.ref).startswith('<Reference')).is_True()
        expect(repr(self.ref.object).startswith('<Git Object')).is_True()

    def test_delete(self):
        self.response('', 204)
        self.delete(self.api)

        with expect.githuberror():
            self.ref.delete()

        self.not_called()
        self.login()
        expect(self.ref.delete()).is_True()
        self.mock_assertions()

    def test_update(self):
        self.response('ref', 200)
        self.patch(self.api)
        self.conf = {
            'data': {
                'sha': 'fakesha',
                'force': True,
            }
        }

        with expect.githuberror():
            self.ref.update('fake')

        self.not_called()
        self.login()
        expect(self.ref.update('fakesha', True)).is_True()
        self.mock_assertions()

        self.response('', 404)
        expect(self.ref.update('fakesha', True)).is_False()
        self.mock_assertions()


class TestTree(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestTree, self).__init__(methodName)
        self.tree = github3.git.Tree(load('tree'))
        self.api = ('https://api.github.com/repos/sigmavirus24/github3.py/git/'
                    'trees/75b347329e3fc87ac78895ca1be58daff78872a1')

    def setUp(self):
        super(TestTree, self).setUp()
        self.tree = github3.git.Tree(self.tree.to_json(), self.g)

    def test_recurse(self):
        self.response('tree', 200)
        self.get(self.api)
        self.conf = {'params': {'recursive': '1'}}

        t = self.tree.recurse()
        expect(t).isinstance(github3.git.Tree)
        expect(repr(t).startswith('<Tree')).is_True()
        self.mock_assertions()

        expect(t.tree[0]).isinstance(github3.git.Hash)
        expect(repr(t.tree[0]).startswith('<Hash')).is_True()
