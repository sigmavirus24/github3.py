import github3
from github3.issues.comment import IssueComment
from github3.issues.event import IssueEvent
from github3.issues.label import Label
from github3.issues import Issue
from tests.utils import BaseCase, load, mock


class TestIssue(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestIssue, self).__init__(methodName)
        self.i = Issue(load('issue'))
        self.api = ("https://api.github.com/repos/sigmavirus24/github3.py/"
                    "issues/1")

    def setUp(self):
        super(TestIssue, self).setUp()
        self.i = Issue(self.i.as_dict(), self.g)

    def test_equality(self):
        i = Issue(load('issue'))
        assert self.i == i
        i._uniq = 1
        assert self.i != i

    def test_repr(self):
        assert repr(self.i) == '<Issue [sigmavirus24/github3.py #1]>'

    def test_add_labels(self):
        self.response('label', 200, _iter=True)
        self.post(self.api + '/labels')
        self.conf = {'data': '["enhancement"]'}

        self.assertRaises(github3.GitHubError, self.i.add_labels, 'foo')

        self.not_called()
        self.login()
        labels = self.i.add_labels('enhancement')
        assert labels != []
        assert isinstance(labels[0], Label)
        self.mock_assertions()

    def test_assign(self):
        self.assertRaises(github3.GitHubError, self.i.assign, 'foo')

        self.login()

        with mock.patch.object(Issue, 'edit') as ed:
            ed.return_value = True
            assert self.i.assign(None) is False
            self.not_called()
            assert self.i.assign('sigmavirus24')
            n = self.i.milestone.number if self.i.milestone else None
            labels = [str(l) for l in self.i.original_labels]
            ed.assert_called_once_with(
                self.i.title, self.i.body, 'sigmavirus24', self.i.state, n,
                labels
            )

    def test_close(self):
        self.assertRaises(github3.GitHubError, self.i.close)

        self.not_called()
        self.login()

        with mock.patch.object(Issue, 'edit') as ed:
            ed.return_value = True
            assert self.i.close()
            u = self.i.assignee.login if self.i.assignee else ''
            n = self.i.milestone.number if self.i.milestone else None
            l = [str(label) for label in self.i.original_labels]
            ed.assert_called_once_with(
                self.i.title, self.i.body, u, self.i.state, n, l
            )

    def test_comment(self):
        self.response('issue_comment')
        self.get(self.api[:-1] + 'comments/476476')

        c = self.i.comment('476476')
        assert isinstance(c, IssueComment)
        assert repr(c).startswith('<Issue Comment')
        self.mock_assertions()

    def test_create_comment(self):
        self.response('issue_comment', 201)
        self.post(self.api + '/comments')
        self.conf = {'data': {'body': 'comment body'}}

        self.assertRaises(github3.GitHubError, self.i.create_comment, '')

        self.login()
        assert isinstance(self.i.create_comment('comment body'), IssueComment)
        self.mock_assertions()

    def test_edit(self):
        self.response('issue', 200)
        self.patch(self.api)
        self.conf = {'data': {'title': 'new title', 'milestone': None}}

        self.assertRaises(github3.GitHubError, self.i.edit)

        self.login()
        assert self.i.edit() is False
        self.not_called()

        assert self.i.edit('new title', milestone=0)
        self.mock_assertions()

    def test_is_closed(self):
        assert self.i.is_closed()

        self.i.closed_at = None
        assert self.i.is_closed()

        self.i.state = 'open'
        assert self.i.is_closed() is False

    def test_remove_label(self):
        self.response('', 204)
        self.delete(self.api + '/labels/name')

        self.assertRaises(github3.GitHubError, self.i.remove_label, 'name')

        self.not_called()
        self.login()
        assert self.i.remove_label('name')
        self.mock_assertions()

    def test_remove_all_labels(self):
        self.assertRaises(github3.GitHubError, self.i.remove_all_labels)

        self.login()

        with mock.patch.object(Issue, 'replace_labels') as rl:
            rl.return_value = []
            assert self.i.remove_all_labels() == []
            rl.assert_called_once_with([])

    def test_replace_labels(self):
        self.response('label', _iter=True)
        self.put(self.api + '/labels')
        self.conf = {'data': '["foo", "bar"]'}

        self.assertRaises(github3.GitHubError, self.i.replace_labels, [])

        self.not_called()
        self.login()

        labels = self.i.replace_labels(['foo', 'bar'])
        assert labels != []
        assert isinstance(labels[0], Label)

    def test_reopen(self):
        self.assertRaises(github3.GitHubError, self.i.reopen)

        self.login()
        n = self.i.milestone.number if self.i.milestone else None
        u = self.i.assignee.login if self.i.assignee else None

        with mock.patch.object(Issue, 'edit') as ed:
            ed.return_value = True
            assert self.i.reopen()
            labels = [str(l) for l in self.i.original_labels]
            ed.assert_called_once_with(
                self.i.title, self.i.body, u, 'open', n, labels
            )

    def test_enterprise(self):
        Issue(load('issue_enterprise'))

    def test_issue_137(self):
        """
        GitHub sometimes returns `pull` as part of of the `html_url` for Issue
        requests.
        """
        i = Issue(load('issue_137'))
        self.assertEqual(
            i.html_url,
            "https://github.com/sigmavirus24/github3.py/pull/1")
        self.assertEqual(i.repository, ("sigmavirus24", "github3.py"))


class TestIssueEvent(BaseCase):
    def setUp(self):
        super(TestIssueEvent, self).setUp()
        self.ev = IssueEvent(load('issue_event'))

    def test_repr(self):
        assert repr(self.ev) == '<Issue Event [{0} by {1}]>'.format(
            'closed', 'sigmavirus24'
        )

    def test_equality(self):
        e = IssueEvent(load('issue_event'))
        assert self.ev == e
        e._uniq = 'fake'
        assert self.ev != e
