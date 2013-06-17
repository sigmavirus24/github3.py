import github3
from tests.utils import BaseCase, expect, load
from unittest import TestCase


class TestEvent(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestEvent, self).__init__(methodName)
        self.ev = github3.events.Event(load('event'))
        self.o = load('org')

    def setUp(self):
        super(TestEvent, self).setUp()
        self.ev = github3.events.Event(self.ev.to_json())

    def test_equality(self):
        e = github3.events.Event(load('event'))
        expect(self.ev) == e
        e.id = 1
        expect(self.ev) != e

    def test_org(self):
        json = self.ev.to_json().copy()
        json['org'] = self.o
        ev = github3.events.Event(json)
        expect(ev.org).isinstance(github3.orgs.Organization)

    def test_repr(self):
        expect(repr(self.ev).startswith('<Event')).is_True()

    def test_list_types(self):
        Event, handlers = (github3.events.Event,
                           github3.events._payload_handlers)
        expect(Event.list_types()) == sorted(handlers.keys())

    def test_is_public(self):
        expect(self.ev.is_public()) == self.ev.public


class TestPayloadHandlers(TestCase):
    def test_commitcomment(self):
        comment = {'comment': load('repo_comment')}
        comment = github3.events._commitcomment(comment)
        expect(comment['comment']).isinstance(
            github3.repos.comment.RepoComment)

    def test_download(self):
        dl = {'download': load('download')}
        dl = github3.events._download(dl)
        expect(dl['download']).isinstance(github3.repos.download.Download)

    def test_follow(self):
        f = {'target': load('user')}
        github3.events._follow(f)
        expect(f['target']).isinstance(github3.users.User)

    def test_forkev(self):
        f = {'forkee': load('repo')}
        github3.events._forkev(f)
        expect(f['forkee']).isinstance(github3.repos.Repository)

    def test_gist(self):
        g = {'gist': load('gist')}
        github3.events._gist(g)
        expect(g['gist']).isinstance(github3.gists.Gist)

    def test_issuecomm(self):
        c = {'issue': load('issue'), 'comment': load('issue_comment')}
        github3.events._issuecomm(c)
        expect(c['issue']).isinstance(github3.issues.Issue)
        expect(c['comment']).isinstance(github3.issues.comment.IssueComment)

    def test_issueevent(self):
        c = {'issue': load('issue')}
        github3.events._issueevent(c)
        expect(c['issue']).isinstance(github3.issues.Issue)

    def test_member(self):
        m = {'member': load('user')}
        github3.events._member(m)
        expect(m['member']).isinstance(github3.users.User)

    def test_pullreqev(self):
        p = {'pull_request': load('pull')}
        github3.events._pullreqev(p)
        expect(p['pull_request']).isinstance(github3.pulls.PullRequest)

    def test_pullreqcomm(self):
        p = {'comment': load('review_comment')}
        github3.events._pullreqcomm(p)
        expect(p['comment']).isinstance(github3.pulls.ReviewComment)

    def test_team(payload):
        t = {'team': load('team'), 'repo': load('repo'), 'user': load('user')}
        github3.events._team(t)
        expect(t['team']).isinstance(github3.orgs.Team)
        expect(t['repo']).isinstance(github3.repos.Repository)
        expect(t['user']).isinstance(github3.users.User)
