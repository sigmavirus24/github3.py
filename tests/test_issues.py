import github3
import datetime
from tests.utils import BaseCase, load, expect


class TestLabel(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestLabel, self).__init__(methodName)
        self.l = github3.issues.Label(load('label'))
        self.api = ("https://api.github.com/repos/sigmavirus24/github3.py/"
                    "labels/bug")

    def setUp(self):
        super(TestLabel, self).setUp()
        self.l = github3.issues.Label(self.l.to_json(), self.g)

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
        self.m = github3.issues.Milestone(load('milestone'))
        self.api = ("https://api.github.com/repos/kennethreitz/requests/"
                    "milestones/18")

    def setUp(self):
        super(TestMilestone, self).setUp()
        self.m = github3.issues.Milestone(self.m.to_json(), self.g)

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
        m = github3.issues.Milestone(json)
        expect(m.due_on).isinstance(datetime.datetime)

    def test_iter_labels(self):
        self.response('label', _iter=True)
        self.get(self.api + '/labels')

        i = self.m.iter_labels()
        expect(i).isinstance(github3.structs.GitHubIterator)
        expect(next(i)).isinstance(github3.issues.Label)
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
                             '2013-12-31TZ23:59:59Z')).is_True()
        self.mock_assertions()


class TestIssue(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestIssue, self).__init__(methodName)
        self.i = github3.issues.Issue(load('issue'))
        self.api = ("https://api.github.com/repos/sigmavirus24/github3.py/"
                    "issues/1")

    def setUp(self):
        super(TestIssue, self).setUp()
        self.i = github3.issues.Issue(self.i.to_json(), self.g)

    def test_repr(self):
        expect(repr(self.i)) == '<Issue [sigmavirus24/github3.py #1]>'
