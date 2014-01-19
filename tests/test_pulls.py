import github3
from mock import patch
from tests.utils import BaseCase, load


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
        assert self.pull == p
        p._uniq = 'foo'
        assert self.pull != p

    def test_hashing(self):
        p = github3.pulls.PullRequest(load('pull'))
        s = set()
        s.add(p)
        s.add(p)
        assert len(s) == 1

    def test_dest(self):
        assert repr(self.pull.base).startswith('<Base')

    def test_repr(self):
        assert repr(self.pull).startswith('<Pull Request')

    def test_close(self):
        self.assertRaises(github3.GitHubError, self.pull.close)

        self.login()

        with patch.object(github3.pulls.PullRequest, 'update') as up:
            up.return_value = True
            assert self.pull.close()
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

        assert self.pull.diff() != ''
        self.mock_assertions()

    def test_is_merged(self):
        self.response('', 204)
        self.get(self.api + '/merge')

        assert self.pull.is_merged()
        self.mock_assertions()

        self.response('', 404)
        assert self.pull.is_merged() is False
        self.mock_assertions()

    def test_iter_comments(self):
        self.response('review_comment', _iter=True)
        self.get(self.api + '/comments')

        c = next(self.pull.iter_comments())
        assert isinstance(c, github3.pulls.ReviewComment)
        self.mock_assertions()

        assert repr(c).startswith('<Review Comment')

    def test_iter_issue_comments(self):
        pull = github3.pulls.PullRequest(load('pull19'))
        self.response('pull19_comment', _iter=True)
        self.get(pull.links['comments'])

        c = next(pull.iter_issue_comments())
        assert isinstance(c, github3.issues.comment.IssueComment)
        self.mock_assertions()

        assert repr(c).startswith('<Issue Comment')

    def test_iter_comits(self):
        self.response('commit', _iter=True)
        self.get(self.api + '/commits')

        assert isinstance(next(self.pull.iter_commits()), github3.git.Commit)
        self.mock_assertions()

    def test_iter_files(self):
        self.response('pull_file', _iter=True)
        self.get(self.api + '/files')

        f = next(self.pull.iter_files())
        assert isinstance(f, github3.pulls.PullFile)
        self.mock_assertions()

        assert repr(f).startswith('<Pull Request File')

    def test_merge(self):
        self.response('merge', 200)
        self.put(self.api + '/merge')
        self.conf = {'data': None}

        self.assertRaises(github3.GitHubError, self.pull.merge)

        self.not_called()
        self.login()
        assert self.pull.merge()
        self.mock_assertions()

        self.conf['data'] = {'commit_message': 'Merged'}
        assert self.pull.merge('Merged')
        self.mock_assertions()

    def test_patch(self):
        self.response('archive', 200)
        self.get(self.api)
        self.conf = {'headers': {'Accept': 'application/vnd.github.patch'}}

        assert self.pull.patch() != ''
        self.mock_assertions()

    def test_reopen(self):
        self.assertRaises(github3.GitHubError, self.pull.reopen)

        self.login()
        with patch.object(github3.pulls.PullRequest, 'update') as up:
            self.pull.reopen()
            up.assert_called_once_with(
                self.pull.title, self.pull.body, 'open')

    def test_update(self):
        self.response('pull', 200)
        self.patch(self.api)
        self.conf = {'data': {'title': 't', 'body': 'b', 'state': 'open'}}

        self.assertRaises(github3.GitHubError, self.pull.update)

        self.login()
        assert self.pull.update() is False
        self.not_called()

        assert self.pull.update('t', 'b', 'open')
        self.mock_assertions()

    def test_enterprise(self):
        github3.pulls.PullRequest(load('pull_enterprise'))

    def test_pull_request_issues(self):
        pr = github3.pulls.PullRequest(load('pull_request'))
        self.assertEqual(pr.issue_url,
                         'https://github.com/sigmavirus24/github3.py/pull/135')
