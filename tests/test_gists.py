from github3 import gists
from tests.utils import (expect, BaseCase, load)


class TestGist(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestGist, self).__init__(methodName)
        self.gist = gists.Gist(load('gist'))
        self.api = 'https://api.github.com/gists/3813862'

    def setUp(self):
        super(TestGist, self).setUp()
        self.gist = gists.Gist(self.gist.to_json(), self.g)

    def test_str(self):
        expect(str(self.gist)) == str(self.gist.id)

    def test_repr(self):
        expect(repr(self.gist)) == '<Gist [{0}]>'.format(self.gist)

    def test_create_comment(self):
        self.response('gist_comment', 201)
        self.post(self.api + '/comments')
        self.conf = {'data': {'body': 'bar'}}

        with expect.githuberror():
            self.gist.create_comment(None)

        self.login()

        expect(self.gist.create_comment(None)).is_None()
        expect(self.gist.create_comment('')).is_None()
        self.not_called()
        expect(self.gist.create_comment('bar')).isinstance(
            gists.comment.GistComment)
        self.mock_assertions()

    def test_delete(self):
        self.response('', 204)
        self.delete(self.api)
        self.conf = {}

        with expect.githuberror():
            self.gist.delete()

        self.not_called()
        self.login()
        expect(self.gist.delete()).is_True()
        self.mock_assertions()

    def test_edit(self):
        self.response('gist', 200)
        self.patch(self.api)
        self.conf = {
            'data': {
                'description': 'desc',
                'files': {'file1': {'content': 'foo bar'}}
            }
        }

        with expect.githuberror():
            self.gist.edit(None, None)

        self.login()
        expect(self.gist.edit()).is_False()
        self.not_called()

        expect(self.gist.edit(**self.conf['data'])).is_True()
        self.mock_assertions()

    def test_fork(self):
        self.response('gist', 201)
        self.post(self.api + '/forks')
        self.conf = {}

        with expect.githuberror():
            self.gist.fork()

        self.not_called()
        self.login()
        expect(self.gist.fork()).isinstance(gists.Gist)
        self.mock_assertions()

    def test_is_public(self):
        expect(self.gist.is_public()) == self.gist.public

    def test_is_starred(self):
        self.response('', 204)
        self.get(self.api + '/star')

        with expect.githuberror():
            self.gist.is_starred()

        self.not_called()
        self.login()
        expect(self.gist.is_starred()).is_True()
        self.mock_assertions()

    def test_iter_comments(self):
        self.response('gist_comment', _iter=True)
        self.get(self.api + '/comments')
        self.conf = {'params': None}

        c = next(self.gist.iter_comments())
        expect(c).isinstance(gists.comment.GistComment)
        self.mock_assertions()

    def test_iter_commits(self):
        self.response('gist_history', _iter=True)
        self.get(self.api + '/commits')
        self.conf = {'params': None}

        h = next(self.gist.iter_commits())
        expect(h).isinstance(gists.history.GistHistory)
        self.mock_assertions()

    def test_iter_files(self):
        gist_file = next(self.gist.iter_files())
        expect(gist_file) == self.gist._files[0]
        expect(gist_file).isinstance(gists.file.GistFile)
        expect(repr(gist_file).startswith('<Gist File')).is_True()

    def test_iter_forks(self):
        with expect.raises(StopIteration):
            expect(next(self.gist.iter_forks()))

    def test_refresh(self):
        self.response('gist', 200)
        self.get(self.api)

        expect(self.gist.refresh() is self.gist).is_True()
        self.mock_assertions()

    def test_star(self):
        self.response('', 204)
        self.put(self.api + '/star')
        self.conf = {}

        with expect.githuberror():
            self.gist.star()

        self.not_called()
        self.login()
        expect(self.gist.star()).is_True()
        self.mock_assertions()

    def test_unstar(self):
        self.response('', 204)
        self.delete(self.api + '/unstar')
        self.conf = {}

        with expect.githuberror():
            self.gist.unstar()

        self.not_called()
        self.login()
        expect(self.gist.unstar()).is_True()
        self.mock_assertions()

    # As opposed to creating an all new class for this
    def test_history(self):
        hist = self.gist.history[0]
        self.response('gist', 200)
        self.get(hist._api)

        expect(hist).isinstance(gists.history.GistHistory)
        expect(hist.get_gist()).isinstance(gists.Gist)
        self.mock_assertions()

        expect(repr(hist).startswith('<Gist History')).is_True()

    def test_equality(self):
        g = gists.Gist(load('gist'))
        expect(self.gist) == g
        g.id = 1
        expect(self.gist) != g


class TestGistComment(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestGistComment, self).__init__(methodName)
        self.comment = gists.comment.GistComment(load('gist_comment'))
        self.api = "https://api.github.com/gists/4321394/comments/655725"

    def setUp(self):
        super(TestGistComment, self).setUp()
        self.comment = gists.comment.GistComment(self.comment.to_json(),
                                                 self.g)

    def test_equality(self):
        c = gists.comment.GistComment(load('gist_comment'))
        expect(self.comment) == c
        c.id = 1
        expect(self.comment) != c

    def test_repr(self):
        expect(repr(self.comment)) != ''

    def test_edit(self):
        self.response('gist_comment', 200)
        self.patch(self.api)
        self.conf = {'data': {'body': 'body'}}

        with expect.githuberror():
            self.comment.edit(None)

        self.login()
        expect(self.comment.edit(None)).is_False()
        self.not_called()

        expect(self.comment.edit('body')).is_True()
        self.mock_assertions()


class TestGistHistory(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestGistHistory, self).__init__(methodName)
        self.hist = gists.history.GistHistory(load('gist_history'))

    def test_equality(self):
        h = gists.history.GistHistory(load('gist_history'))
        expect(self.hist) == h
        h.version = 'foo'
        expect(self.hist) != h
