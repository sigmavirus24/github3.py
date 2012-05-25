"""
github3.event
=============

This module contains the class(es) related to Events

"""

from .compat import loads
from .models import GitHubCore, User
from .repo import Repository


class Event(BaseEvent):
    def __init__(self, event):
        super(BaseEvent, self).__init__(event)
        self._type = event.get('type')

    def __repr__(self):
        return '<Event [%s]>' % self._type[:-5]
