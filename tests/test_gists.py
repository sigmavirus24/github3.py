import github3
from tests.utils import (expect, BaseCase, load)


class TestGist(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestGist, self).__init__(methodName)
        self.gist = github3.gists.Gist(load('gist'))
        self.api = 'https://api.github.com/gists/3813862'

    def setUp(self):
        super(TestGist, self).setUp()
        self.gist = github3.gists.Gist(self.gist.to_json(), self.g)

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
            github3.gists.GistComment)
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
        expect(self.gist.fork()).isinstance(github3.gists.Gist)
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
        self.response('gist_comment', 200, _iter=True)
        self.get(self.api + '/comments')
        self.conf = {'params': None}

        c = next(self.gist.iter_comments())
        expect(c).isinstance(github3.gists.GistComment)
        self.mock_assertions()

    def test_iter_files(self):
        gist_file = next(self.gist.iter_files())
        expect(gist_file) == self.gist._files[0]
        expect(repr(gist_file).startswith('<Gist File')).is_True()

    def test_iter_forks(self):
        with expect.raises(StopIteration):
            expect(next(self.gist.iter_forks()))

    def test_refresh(self):
        self.response('gist', 200)
        self.get(self.api)

        expect(self.gist.refresh()) is self.gist
        self.mock_assertions()

    def test_star(self):
        self.response('', 204)
        self.put(self.api)

        with expect.githuberror():
            self.gist.star()

        self.not_called()
        self.login()
        expect(self.gist.star()).is_True()

    def test_unstar(self):
        self.response('', 204)
        self.delete(self.api)

        with expect.githuberror():
            self.gist.unstar()

        self.not_called()
        self.login()
        expect(self.gist.unstar()).is_True()

    # As opposed to creating an all new class for this
    def test_history(self):
        hist = self.gist.history[0]
        self.response('gist', 200)
        self.get(hist._api)

        expect(hist.get_gist()).isinstance(github3.gists.Gist)
        self.mock_assertions()

        expect(repr(hist).startswith('<Gist History')).is_True()


class TestGistComment(BaseCase):
    def test(self):
        json = load('gist_comment')
        json['user'] = load('user')
        comment = github3.gists.GistComment(json)
        expect(repr(comment).startswith('<Gist Comment')).is_True()
