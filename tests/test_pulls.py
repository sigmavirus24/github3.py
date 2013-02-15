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
        self.response('archive', 200)
        self.get(self.api)
        self.conf = {
            'headers': {
                'Accept': 'application/vnd.github.diff'
            }
        }

        expect(self.pull.diff()) != ''
        self.mock_assertions()
