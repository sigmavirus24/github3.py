# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .. import users
from ..models import GitHubCore


class IssueEvent(GitHubCore):
    """The :class:`IssueEvent <IssueEvent>` object. This specifically deals
    with events described in the
    `Issues\>Events <http://developer.github.com/v3/issues/events>`_ section of
    the GitHub API.

    Two event instances can be checked like so::

        e1 == e2
        e1 != e2

    And is equivalent to::

        e1.commit_id == e2.commit_id
        e1.commit_id != e2.commit_id

    """
    def _update_attributes(self, event):
        # The type of event:
        #   ('closed', 'reopened', 'subscribed', 'merged', 'referenced',
        #    'mentioned', 'assigned')
        #: The type of event, e.g., closed
        self.event = self._get_attribute(event, 'event')
        #: SHA of the commit.
        self.commit_id = self._get_attribute(event, 'commit_id')
        self._api = self._get_attribute(event, 'url')

        #: :class:`Issue <github3.issues.Issue>` where this comment was made.
        from .issue import Issue
        self.issue = self._class_attribute(event, 'issue', Issue, self)

        #: :class:`User <github3.users.User>` who caused this event.
        self.actor = self._class_attribute(
            event, 'actor', users.ShortUser, self,
        )

        #: Number of comments
        self.comments = self._get_attribute(event, 'comments')

        #: datetime object representing when the event was created.
        self.created_at = self._strptime_attribute(event, 'created_at')

        #: Dictionary of links for the pull request
        self.pull_request = self._get_attribute(event, 'pull_request', {})

        #: Dictionary containing label details
        self.label = self._get_attribute(event, 'label', {})

        #: The integer ID of the event
        self.id = self._get_attribute(event, 'id')

        #: :class:`User <github3.users.User>` that is assigned
        self.assignee = self._class_attribute(
            event, 'assignee', users.ShortUser, self,
        )

        #: Dictionary containing milestone details
        self.milestone = self._get_attribute(event, 'milestone', {})

        #: Dictionary containing to and from attributes
        self.rename = self._get_attribute(event, 'rename', {})

        self._uniq = self.commit_id

    def _repr(self):
        return '<Issue Event [{0} by {1}]>'.format(
            self.event, self.actor
        )
