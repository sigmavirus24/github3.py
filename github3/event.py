"""
github3.event
=============

This module contains the class(es) related to Events

"""

from .compat import loads
from .git import Commit
from .models import GitHubCore, BaseEvent
from .repo import Repository
from .user import User


class Event(BaseEvent):
    # Based upon self._type, choose a function to determine
    # self._payload
    _payload_handlers = {
            'CommitCommentEvent': self._commitcomment,
            'CreateEvent': self._create,
            'DeleteEvent': self._delete,
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

    def __init__(self, event, session):
        super(Event, self).__init__(event, session)
        self._type = event.get('type')
        self._public = event.get('public')
        self._repo = Repository(event.get('repo'), self._session)
        self._actor = User(event.get('actor'), self._session)
        self._id = event.get('id')
        self._payload = event.get('payload')

        # Commented out for now because there is no Organization class
        self._org = None
        if event.get('org'):
            self._org = Organization(event.get('org'), self._session)

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

    # @property
    # def payload(self):
    #     return self._payload

    def is_public(self):
        return self._public

    @property
    def repo(self):
        return self._repo

    @property
    def type(self):
        return self._type

    def _commitcomment(self, comment):
        from .repo import RepoComment
        return RepoComment(comment, self._session) if comment else None

    def _create(self, create):
        return CreateEvent(create) if create else None

    def _delete(self, delete):
        return DeleteEvent(delete) if delete else None

    def _download(self, download):
        return DownloadEvent(download) if download else None


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
