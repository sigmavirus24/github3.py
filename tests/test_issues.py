import github3
from github3.issues.comment import IssueComment
from github3.issues.event import IssueEvent
from github3.issues.label import Label
from github3.issues.milestone import Milestone
from github3.issues import Issue
import datetime
from tests.utils import BaseCase, load, expect
from mock import patch


class TestLabel(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestLabel, self).__init__(methodName)
        self.l = Label(load('label'))
        self.api = ("https://api.github.com/repos/sigmavirus24/github3.py/"
                    "labels/bug")

    def setUp(self):
        super(TestLabel, self).setUp()
        self.l = Label(self.l.to_json(), self.g)

    def test_equality(self):
        l = Label(load('label'))
        expect(self.l) == l
        l._api = "https://api.github.com/repos/sigmavirus24/github3.py/labels/wontfix"
        expect(self.l) != l

    def test_repr(self):
        expect(repr(self.l)) == '<Label [{0}]>'.format(self.l.name)

    def test_str(self):
        expect(str(self.l)) == self.l.name

    def test_delete(self):
        self.response('', 204)
        self.delete(self.api)

        with expect.githuberror():
            self.l.delete()

        self.not_called()
        self.login()
        expect(self.l.delete()).is_True()

    def test_update(self):
        self.response('label', 200)
        self.patch(self.api)
        self.conf = {'data': {'name': 'newname', 'color': 'afafaf'}}

        with expect.githuberror():
            self.l.update(None, None)

        self.login()
        expect(self.l.update(None, None)).is_False()
        self.not_called()

        expect(self.l.update('newname', 'afafaf')).is_True()
        self.mock_assertions()

        expect(self.l.update('newname', '#afafaf')).is_True()
        self.mock_assertions()


class TestMilestone(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestMilestone, self).__init__(methodName)
        self.m = Milestone(load('milestone'))
        self.api = ("https://api.github.com/repos/kennethreitz/requests/"
                    "milestones/18")

    def setUp(self):
        super(TestMilestone, self).setUp()
        self.m = Milestone(self.m.to_json(), self.g)

    def test_repr(self):
        expect(repr(self.m)) == '<Milestone [v1.0.0]>'

    def test_str(self):
        expect(str(self.m)) == 'v1.0.0'

    def test_delete(self):
        self.response('', 204)
        self.delete(self.api)

        with expect.githuberror():
            self.m.delete()

        self.not_called()
        self.login()
        expect(self.m.delete()).is_True()
        self.mock_assertions()

    def test_due_on(self):
        json = self.m.to_json().copy()
        json['due_on'] = '2012-12-31T23:59:59Z'
        m = Milestone(json)
        expect(m.due_on).isinstance(datetime.datetime)

    def test_iter_labels(self):
        self.response('label', _iter=True)
        self.get(self.api + '/labels')

        i = self.m.iter_labels()
        expect(i).isinstance(github3.structs.GitHubIterator)
        expect(next(i)).isinstance(Label)
        self.mock_assertions()

    def test_update(self):
        self.response('milestone', 200)
        self.patch(self.api)
        self.conf = {
            'data': {
                'title': 'foo',
                'state': 'closed',
                'description': ':sparkles:',
                'due_on': '2013-12-31T23:59:59Z'
            }
        }

        with expect.githuberror():
            self.m.update(None)

        self.login()
        expect(self.m.update(None)).is_False()
        self.not_called()

        expect(self.m.update('foo', 'closed', ':sparkles:',
                             '2013-12-31T23:59:59Z')).is_True()
        self.mock_assertions()


class TestIssue(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestIssue, self).__init__(methodName)
        self.i = Issue(load('issue'))
        self.api = ("https://api.github.com/repos/sigmavirus24/github3.py/"
                    "issues/1")

    def setUp(self):
        super(TestIssue, self).setUp()
        self.i = Issue(self.i.to_json(), self.g)

    def test_equality(self):
        i = Issue(load('issue'))
        expect(self.i) == i
        i.id = 1
        expect(self.i) != i

    def test_repr(self):
        expect(repr(self.i)) == '<Issue [sigmavirus24/github3.py #1]>'

    def test_add_labels(self):
        self.response('label', 200, _iter=True)
        self.post(self.api + '/labels')
        self.conf = {'data': '["enhancement"]'}

        with expect.githuberror():
            self.i.add_labels('foo')

        self.not_called()
        self.login()
        labels = self.i.add_labels('enhancement')
        expect(labels) != []
        expect(labels[0]).isinstance(Label)
        self.mock_assertions()

    def test_assign(self):
        with expect.githuberror():
            self.i.assign('foo')

        self.login()

        with patch.object(Issue, 'edit') as ed:
            ed.return_value = True
            expect(self.i.assign(None)).is_False()
            self.not_called()
            expect(self.i.assign('sigmavirus24')).is_True()
            n = self.i.milestone.number if self.i.milestone else None
            ed.assert_called_once_with(
                self.i.title, self.i.body, 'sigmavirus24', self.i.state, n,
                self.i.labels
            )

    def test_close(self):
        with expect.githuberror():
            self.i.close()

        self.not_called()
        self.login()

        with patch.object(Issue, 'edit') as ed:
            ed.return_value = True
            expect(self.i.close()).is_True()
            u = self.i.assignee.login if self.i.assignee else ''
            n = self.i.milestone.number if self.i.milestone else None
            ed.assert_called_once_with(
                self.i.title, self.i.body, u, self.i.state, n, self.i.labels
            )

    def test_comment(self):
        self.response('issue_comment')
        self.get(self.api[:-1] + 'comments/476476')

        c = self.i.comment('476476')
        expect(c).isinstance(IssueComment)
        expect(repr(c).startswith('<Issue Comment')).is_True()
        self.mock_assertions()

    def test_create_comment(self):
        self.response('issue_comment', 201)
        self.post(self.api + '/comments')
        self.conf = {'data': {'body': 'comment body'}}

        with expect.githuberror():
            self.i.create_comment('')

        self.login()
        expect(self.i.create_comment(None)).is_None()
        self.not_called()

        expect(self.i.create_comment('comment body')).isinstance(IssueComment)
        self.mock_assertions()

    def test_edit(self):
        self.response('issue', 200)
        self.patch(self.api)
        self.conf = {'data': {'title': 'new title'}}

        with expect.githuberror():
            self.i.edit()

        self.login()
        expect(self.i.edit()).is_False()
        self.not_called()

        expect(self.i.edit('new title')).is_True()
        self.mock_assertions()

    def test_is_closed(self):
        expect(self.i.is_closed()).is_True()

        self.i.closed_at = None
        expect(self.i.is_closed()).is_True()

        self.i.state = 'open'
        expect(self.i.is_closed()).is_False()

    def test_iter_comments(self):
        self.response('issue_comment', _iter=True)
        self.get(self.api + '/comments')

        expect(next(self.i.iter_comments())).isinstance(IssueComment)
        self.mock_assertions()

    def test_iter_events(self):
        self.response('issue_event', _iter=True)
        self.get(self.api + '/events')

        e = next(self.i.iter_events())
        expect(e).isinstance(IssueEvent)
        expect(repr(e).startswith('<Issue Event')).is_True()
        self.mock_assertions()

    def test_remove_label(self):
        self.response('', 204)
        self.delete(self.api + '/labels/name')

        with expect.githuberror():
            self.i.remove_label('name')

        self.not_called()
        self.login()
        expect(self.i.remove_label('name')).is_True()
        self.mock_assertions()

    def test_remove_all_labels(self):
        with expect.githuberror():
            self.i.remove_all_labels()

        self.login()

        with patch.object(Issue, 'replace_labels') as rl:
            rl.return_value = []
            expect(self.i.remove_all_labels()) == []
            rl.assert_called_once_with([])

    def test_replace_labels(self):
        self.response('label', _iter=True)
        self.put(self.api + '/labels')
        self.conf = {'data': '["foo", "bar"]'}

        with expect.githuberror():
            self.i.replace_labels([])

        self.not_called()
        self.login()

        labels = self.i.replace_labels(['foo', 'bar'])
        expect(labels) != []
        expect(labels[0]).isinstance(Label)

    def test_reopen(self):
        with expect.githuberror():
            self.i.reopen()

        self.login()
        n = self.i.milestone.number if self.i.milestone else None
        u = self.i.assignee.login if self.i.assignee else None

        with patch.object(Issue, 'edit') as ed:
            ed.return_value = True
            expect(self.i.reopen()).is_True()
            ed.assert_called_once_with(
                self.i.title, self.i.body, u, 'open', n, self.i.labels
            )


class TestIssueEvent(BaseCase):
    def setUp(self):
        super(TestIssueEvent, self).setUp()
        self.ev = IssueEvent(load('issue_event'))

    def test_equality(self):
        e = IssueEvent(load('issue_event'))
        expect(self.ev) == e
        e.commit_id = 'fake'
        expect(self.ev) != e
