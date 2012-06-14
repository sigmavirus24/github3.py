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
            'PublicEvent': None,
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
        pass

    def _delete(self, delete):
        pass
