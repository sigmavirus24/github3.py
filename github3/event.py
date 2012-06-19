"""
github3.event
=============

This module contains the class(es) related to Events

"""

from .git import Commit
from .models import GitHubCore, BaseEvent
from .repo import Repository
from .user import User
from .org import Organization


class Event(BaseEvent):
    def __init__(self, event, session):
        super(Event, self).__init__(event, session)
        self._type = event.get('type')
        self._public = event.get('public')
        self._repo = event.get('repo', {})
        self._actor = event.get('actor', {})
        self._id = event.get('id')
        self._payload = event.get('payload')
        self._org = event.get('org', {})

    def __repr__(self):
        return '<Event [%s]>' % self._type[:-5]

    @property
    def actor(self):
        return self._actor

    @classmethod
    def list_types(cls):
        return sorted(cls._payload_handlers.keys())

    @property
    def org(self):
        return self._org

    @property
    def payload(self):
        return self._payload

    def is_public(self):
        return self._public

    @property
    def repo(self):
        return self._repo

    @property
    def type(self):
        return self._type


def _commitcomment(comment):
    from .repo import RepoComment
    return RepoComment(comment, None) if comment else None


def _create(create):
    return CreateEvent(create) if create else None


def _delete(delete):
    return DeleteEvent(delete) if delete else None


def _download(download):
    return DownloadEvent(download) if download else None


def _follow(follow):
    return FollowEvent(follow) if follow else None


def _forkev(fork):
    return ForkEvent(fork) if fork else None


def _forkapply(fork):
    return ForkApplyEvent(fork) if fork else None


def _gist(gist):
    return GistEvent(gist) if gist else None


def _gollum(event):
    return GollumEvent(event) if event else None


def _issuecomm(event):
    return IssueCommentEvent(event) if event else None


def _issueevent(event):
    return IssueEvent(event) if event else None


def _member(event):
    return MemberEvent(event) if event else None


def _pullreqev(event):
    return PullRequestEvent(event) if event else None


# Based upon self._type, choose a function to determine
# self._payload
_payload_handlers = {
        'CommitCommentEvent': _commitcomment,
        'CreateEvent': _create,
        'DeleteEvent': _delete,
        'DownloadEvent': None,
        'FollowEvent': None,
        'ForkEvent': None,
        'ForkApplyEvent': None,
        'GistEvent': None,
        'GollumEvent': None,
        'IssueCommentEvent': None,
        'IssueEvent': None,
        'MemberEvent': None,
        'PublicEvent': lambda x: '',
        'PullRequestEvent': None,
        'PullRequestCommentReviewEvent': None,
        'PushEvent': None,
        'TeamAddEvent': None,
        'WatchEvent': None,
        }


class CreateEvent(object):
    def __init__(self, event):
        super(CreateEvent, self).__init__()
        self._reft = event.get('ref_type', '')
        self._ref = event.get('ref', '')
        self._branch = event.get('master_branch', '')
        self._desc = event.get('description', '')

    def __repr__(self):
        return '<CreateEvent [%s on %s]>' % (self._reft, self._branch)

    @property
    def description(self):
        return self._desc

    @property
    def master_branch(self):
        return self._branch

    @property
    def ref(self):
        return self._ref

    @property
    def ref_type(self):
        return self._reft


class DeleteEvent(object):
    def __init__(self, event):
        super(DeleteEvent, self).__init__()
        self._reft = event.get('ref_type', '')
        self._ref = event.get('ref', '')

    def __repr__(self):
        return '<DeleteEvent [%s]>' % self._reft

    @property
    def ref(self):
        return self._ref

    @property
    def ref_type(self):
        return self._reft


class DownloadEvent(object):
    def __init__(self, event):
        super(DownloadEvent, self).__init__()
        from .repo import Download
        self._dl = Download(event.get('download', {}), None)

    def __repr__(self):
        return '<DownloadEvent [%s]>' % self._dl.name

    @property
    def download(self):
        return self._dl


class FollowEvent(object):
    def __init__(self, event):
        super(FollowEvent, self).__init__()
        from .user import User
        self._tgt = User(event.get('target', {}), None)

    def __repr__(self):
        return '<FollowEvent [%s]>' % self._tgt.login

    @property
    def target(self):
        return self._tgt


class ForkEvent(object):
    def __init__(self, event):
        super(ForkEvent, self).__init__()
        from .repo import Repository
        self._forkee = Repository(event.get('forkee', {}), None)

    def __repr__(self):
        return '<ForkEvent [%s]>' % self._forkee.name

    @property
    def forkee(self):
        return self._forkee


class ForkApplyEvent(object):
    def __init__(self, event):
        super(ForkApplyEvent, self).__init__()
        self._head = event.get('head', '')
        self._before = event.get('before', '')
        self._after = event.get('after', '')

    def __repr__(self):
        return '<ForkApplyEvent [%s]>' % self._head

    @property
    def after(self):
        return self._after

    @property
    def before(self):
        return self._before

    @property
    def head(self):
        return self._head


class GistEvent(object):
    def __init__(self, event):
        super(GistEvent, self).__init__()
        from .gist import Gist
        self._act = event.get('action', '')
        self._gist = Gist(event.get('gist', {}), None)

    def __repr__(self):
        return '<GistEvent [%s]>' % self._gist.id

    @property
    def action(self):
        return self._act

    @property
    def gist(self):
        return self._gist
    

class GollumEvent(object):
    def __init__(self, event):
        super(GollumEvent, self).__init__()
        pages = event.get('pages')
        self._sha = pages.get('sha', '')
        self._title = pages.get('title', '')
        self._act = pages.get('action', '')
        self._pg = pages.get('page_name', '')
        self._summary = pages.get('summary', '')
        self._url = pages.get('html_url', '')
        self._pgs = pages

    def __repr__(self):
        return '<GollumEvent [%s %s]>' % (self._act, self._pg)

    @property
    def action(self):
        return self._act

    @property
    def html_url(self):
        return self._url

    @property
    def page_name(self):
        return self._pg

    @property
    def pages(self):
        return self._pgs

    @property
    def sha(self):
        return self._sha

    @property
    def summary(self):
        return self._summary

    @property
    def title(self):
        return self._title


class IssueCommentEvent(object):
    def __init__(self, event):
        super(IssueCommentEvent, self).__init__()
        from .issue import Issue, IssueComment
        self._act = event.get('action', '')
        self._iss = Issue(event.get('issue', {}), None)
        self._ic = IssueComment(event.get('comment', {}), None)

    def __repr__(self):
        return '<IssueCommentEvent [%s on %d]>' % (self._act, 
                self._iss.number)

    @property
    def action(self):
        return self._act

    @property
    def comment(self):
        return self._ic

    @property
    def issue(self):
        return self._iss


class IssuesEvent(object):
    def __init__(self, event):
        super(IssuesEvent, self).__init__()
        from .issue import Issue
        self._act = event.get('action', '')
        self._iss = Issue(event.get('issue', {}), None)

    def __repr__(self):
        return '<IssuesEvent [%s on %d]>' % (self._act, self._iss.number)

    @property
    def action(self):
        return self._act

    @property
    def issue(self):
        return self._iss


class MemberEvent(object):
    def __init__(self, event):
        super(MemberEvent, self).__init__()
        from .user import User
        self._act = event.get('action', '')
        self._mem = User(event.get('member', {}), None)

    def __repr__(self):
        return '<MemberEvent [%s by %s]>' % (self._act, self._mem.login)

    @property
    def action(self):
        return self._act

    @property
    def member(self):
        return self._mem


class PullRequestEvent(object):
    def __init__(self, event):
        super(PullRequestEvent, self).__init__()
        from .pulls import PullRequest
        self._act = event.get('action', '')
        self._num = event.get('number', -1)
        self._pull = PullRequest(event.get('pull_request', {}), None)

    def __repr__(self):
        return '<PullRequestEvent [%s on %s]>' % (self._act, 
                self._pull.number)

    @property
    def action(self):
        return self._act

    @property
    def number(self):
        return self._num

    @property
    def pull_request(self):
        return self._pull


class PullRequestCommentReviewEvent(object):
    def __init__(self, event):
        super(PullRequestCommentReviewEvent, self).__init__()
        from .pulls import ReviewComment
        self._com = ReviewComment(event.get('comment', {}), None)

    def __repr__(self):
        return '<PullRequestCommentReviewEvent [%s]>' % str(self._com.id)

    @property
    def comment(self):
        return self._com


class PushEvent(object):
    def __init__(self, event):
        super(PushEvent, self).__init__()
        self._head = event.get('head', '')
        self._ref = event.get('ref', '')
        self._sz = event.get('size', -1)
        self._commits = event.get('commits', {})
        self._author = event.get('author', {})

    def __repr__(self):
        return '<PushEvent [%s by %s]>' % (self._head, self._authname)

    @property
    def author(self):
        return self._author

    @property
    def commits(self):
        return self._commits

    @property
    def head(self):
        return self._head

    @property
    def ref(self):
        return self._ref

    @property
    def size(self):
        return self._sz


class TeamAddEvent(object):
    def __init__(self, event):
        super(TeamAddEvent, self).__init__()
        from .org import Team
        from .user import User
        from .repo import Repository
        self._team = Team(event.get('team', {}), None)
        self._user = User(event.get('user', {}), None)
        self._repo = Repository(event.get('repo', {}), None)

    def __repr__(self):
        return '<TeamAddEvent [%s]>' % self._team.name

    @property
    def repo(self):
        return self._repo

    @property
    def team(self):
        return self._team

    @property
    def user(self):
        return self._user


def WatchEvent(object):
    def __init__(self, event):
        super(WatchEvent, self).__init__()
        self._act = event.get('action', '')

    def __repr__(self):
        return '<WatchEvent [%s]>' % self._act

    @property
    def action(self):
        return self._act
