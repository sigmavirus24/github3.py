"""
github3.event
=============

This module contains the class(es) related to Events

"""

from .compat import loads
from .models import GitHubCore, BaseEvent
from .repo import Repository
from .user import User


class Event(BaseEvent):
    # Based upon self._type, choose a function to determine
    # self._payload
    _payload_handlers = {
            'CommitCommentEvent': None,
            'CreateEvent': None,
            'DeleteEvent': None,
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

        # Commented out for now because there is no Organization class
        # if event.get('org'):
        #     self._org = Organization(event.get('org'), self._session)

    def __repr__(self):
        return '<Event [%s]>' % self._type[:-5]

    @property
    def actor(self):
        return self._actor

    @classmethod
    def list_types(cls):
        return sorted(cls._payload_handlers.keys())

    # @property
    # def org(self):
    #     return self._org

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
