import github3
from mock import patch
from tests.utils import BaseCase, load, expect


class TestPullRequest(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestPullRequest, self).__init__(methodName)
        self.pull = github3.pulls.PullRequest(load('pull'))
        self.api = ("https://api.github.com/repos/sigmavirus24/github3.py/"
                    "pulls/18")

    def setUp(self):
        super(TestPullRequest, self).setUp()
        self.pull = github3.pulls.PullRequest(self.pull.to_json(), self.g)

    def test_equality(self):
        p = github3.pulls.PullRequest(load('pull'))
        expect(self.pull) == p
        p.id = 'foo'
        expect(self.pull) != p

    def test_dest(self):
        expect(repr(self.pull.base).startswith('<Base')).is_True()

    def test_repr(self):
        expect(repr(self.pull).startswith('<Pull Request'))

    def test_close(self):
        with expect.githuberror():
            self.pull.close()

        self.login()

        with patch.object(github3.pulls.PullRequest, 'update') as up:
            up.return_value = True
            expect(self.pull.close()).is_True()
            up.assert_called_once_with(
                self.pull.title, self.pull.body, 'closed')

    def test_diff(self):
        self.response('archive')
        self.get(self.api)
        self.conf = {
            'headers': {
                'Accept': 'application/vnd.github.diff'
            }
        }

        expect(self.pull.diff()) != ''
        self.mock_assertions()

    def test_is_merged(self):
        self.response('', 204)
        self.get(self.api + '/merge')

        expect(self.pull.is_merged()).is_True()
        self.mock_assertions()

        self.response('', 404)
        expect(self.pull.is_merged()).is_False()
        self.mock_assertions()

    def test_iter_comments(self):
        self.response('review_comment', _iter=True)
        self.get(self.api + '/comments')

        c = next(self.pull.iter_comments())
        expect(c).isinstance(
            github3.pulls.ReviewComment)
        self.mock_assertions()

        expect(repr(c).startswith('<Review Comment')).is_True()

    def test_iter_comits(self):
        self.response('commit', _iter=True)
        self.get(self.api + '/commits')

        expect(next(self.pull.iter_commits())).isinstance(github3.git.Commit)
        self.mock_assertions()

    def test_iter_files(self):
        self.response('pull_file', _iter=True)
        self.get(self.api + '/files')

        f = next(self.pull.iter_files())
        expect(f).isinstance(github3.pulls.PullFile)
        self.mock_assertions()

        expect(repr(f).startswith('<Pull Request File')).is_True()

    def test_merge(self):
        self.response('merge', 200)
        self.put(self.api + '/merge')
        self.conf = {'data': None}

        with expect.githuberror():
            self.pull.merge()

        self.not_called()
        self.login()
        expect(self.pull.merge()).is_True()
        self.mock_assertions()

        self.conf['data'] = {'commit_message': 'Merged'}
        expect(self.pull.merge('Merged')).is_True()
        self.mock_assertions()

    def test_patch(self):
        self.response('archive', 200)
        self.get(self.api)
        self.conf = {'headers': {'Accept': 'application/vnd.github.patch'}}

        expect(self.pull.patch()) != ''
        self.mock_assertions()

    def test_reopen(self):
        with expect.githuberror():
            self.pull.reopen()

        self.login()
        with patch.object(github3.pulls.PullRequest, 'update') as up:
            self.pull.reopen()
            up.assert_called_once_with(
                self.pull.title, self.pull.body, 'open')

    def test_update(self):
        self.response('pull', 200)
        self.patch(self.api)
        self.conf = {'data': {'title': 't', 'body': 'b', 'state': 'open'}}

        with expect.githuberror():
            self.pull.update()

        self.login()
        expect(self.pull.update()).is_False()
        self.not_called()

        expect(self.pull.update('t', 'b', 'open')).is_True()
        self.mock_assertions()
