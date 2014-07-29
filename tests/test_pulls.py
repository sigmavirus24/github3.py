import github3
from tests.utils import BaseCase, load, mock


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

        with mock.patch.object(github3.pulls.PullRequest, 'update') as up:
            up.return_value = True
            assert self.pull.close()
            up.assert_called_once_with(
                self.pull.title, self.pull.body, 'closed')

    def test_reopen(self):
        self.assertRaises(github3.GitHubError, self.pull.reopen)

        self.login()
        with mock.patch.object(github3.pulls.PullRequest, 'update') as up:
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
