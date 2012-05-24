"""
github3.event
=============

This module contains the class(es) related to Events

"""

from .compat import loads
from .models import GitHubCore, User
from .repo import Repository

class BaseEvent(GitHubCore):
    def __init__(self, event, session):
        super(BaseEvent, self).__init__(session)
        # Guaranteed to exist:
        self._event = event.get('event')
        self._actor = User(event.get('actor'), self._session)
        self._created = self._strptime(event.get('created_at'))

        # Not guaranteed to exist
        self._api_url = event.get('url')

    def __repr__(self):
        return '<github3-event at 0x%x>' % id(self)

    @property
    def event(self):
        return self._event

    @property
    def actor(self):
        return self._actor

    @property
    def created_at(self):
        return self._created
