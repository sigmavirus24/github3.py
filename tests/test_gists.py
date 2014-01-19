import github3
from github3 import gists
from tests.utils import (BaseCase, load)


class TestGist(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestGist, self).__init__(methodName)
        self.gist = gists.Gist(load('gist'))
        self.api = 'https://api.github.com/gists/3813862'

    def setUp(self):
        super(TestGist, self).setUp()
        self.gist = gists.Gist(self.gist.to_json(), self.g)

    def test_str(self):
        assert str(self.gist) == str(self.gist.id)

    def test_repr(self):
        assert repr(self.gist) == '<Gist [{0}]>'.format(self.gist)

    def test_create_comment(self):
        self.response('gist_comment', 201)
        self.post(self.api + '/comments')
        self.conf = {'data': {'body': 'bar'}}

        self.assertRaises(github3.GitHubError, self.gist.create_comment)
        self.login()

        assert self.gist.create_comment(None) is None
        assert self.gist.create_comment('') is None
        self.not_called()
        assert isinstance(self.gist.create_comment('bar'),
                          gists.comment.GistComment)
        self.mock_assertions()

    def test_delete(self):
        self.response('', 204)
        self.delete(self.api)
        self.conf = {}

        self.assertRaises(github3.GitHubError, self.gist.delete)

        self.not_called()
        self.login()
        assert self.gist.delete()
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

        self.assertRaises(github3.GitHubError, self.gist.edit)

        self.login()
        assert self.gist.edit() is False
        self.not_called()

        assert self.gist.edit(**self.conf['data'])
        self.mock_assertions()

    def test_fork(self):
        self.response('gist', 201)
        self.post(self.api + '/forks')
        self.conf = {}

        self.assertRaises(github3.GitHubError, self.gist.fork)

        self.not_called()
        self.login()
        assert isinstance(self.gist.fork(), gists.Gist)
        self.mock_assertions()

    def test_is_public(self):
        assert self.gist.is_public() == self.gist.public

    def test_is_starred(self):
        self.response('', 204)
        self.get(self.api + '/star')

        self.assertRaises(github3.GitHubError, self.gist.is_starred)

        self.not_called()
        self.login()
        assert self.gist.is_starred()
        self.mock_assertions()

    def test_iter_comments(self):
        self.response('gist_comment', _iter=True)
        self.get(self.api + '/comments')
        self.conf = {'params': {'per_page': 100}}

        c = next(self.gist.iter_comments())

        assert isinstance(c, gists.comment.GistComment)
        self.mock_assertions()

    def test_iter_commits(self):
        self.response('gist_history', _iter=True)
        self.get(self.api + '/commits')
        self.conf = {'params': {'per_page': 100}}

        h = next(self.gist.iter_commits())
        assert isinstance(h, gists.history.GistHistory)
        self.mock_assertions()

    def test_iter_files(self):
        gist_file = next(self.gist.iter_files())
        assert gist_file == self.gist._files[0]
        assert isinstance(gist_file, gists.file.GistFile)
        assert repr(gist_file).startswith('<Gist File')

    def test_iter_forks(self):
        self.assertRaises(StopIteration, next, self.gist.iter_forks())

    def test_refresh(self):
        self.response('gist', 200)
        self.get(self.api)

        assert self.gist.refresh() is self.gist
        self.mock_assertions()

    def test_star(self):
        self.response('', 204)
        self.put(self.api + '/star')
        self.conf = {}

        self.assertRaises(github3.GitHubError, self.gist.star)

        self.not_called()
        self.login()
        assert self.gist.star()
        self.mock_assertions()

    def test_unstar(self):
        self.response('', 204)
        self.delete(self.api + '/star')
        self.conf = {}

        self.assertRaises(github3.GitHubError, self.gist.unstar)

        self.not_called()
        self.login()
        assert self.gist.unstar()
        self.mock_assertions()

    # As opposed to creating an all new class for this
    def test_history(self):
        hist = self.gist.history[0]
        self.response('gist', 200)
        self.get(hist._api)

        assert isinstance(hist, gists.history.GistHistory)
        assert isinstance(hist.get_gist(), gists.Gist)
        self.mock_assertions()

        assert repr(hist).startswith('<Gist History')

    def test_equality(self):
        g = gists.Gist(load('gist'))
        assert self.gist == g
        g._uniq = 1
        assert self.gist != g


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
        assert self.comment == c
        c._uniq = 1
        assert self.comment != c

    def test_repr(self):
        assert repr(self.comment) != ''

    def test_edit(self):
        self.response('gist_comment', 200)
        self.patch(self.api)
        self.conf = {'data': {'body': 'body'}}

        self.assertRaises(github3.GitHubError, self.comment.edit)

        self.login()
        assert self.comment.edit(None) is False
        self.not_called()

        assert self.comment.edit('body')
        self.mock_assertions()


class TestGistHistory(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestGistHistory, self).__init__(methodName)
        self.hist = gists.history.GistHistory(load('gist_history'))

    def test_equality(self):
        h = gists.history.GistHistory(load('gist_history'))
        assert self.hist == h
        h._uniq = 'foo'
        assert self.hist != h
