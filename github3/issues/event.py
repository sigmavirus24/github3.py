# -*- coding: utf-8 -*-
"""Issue events logic."""
from __future__ import unicode_literals

from .. import users
from ..models import GitHubCore


class IssueEvent(GitHubCore):
    """Representation of an event from a specific issue.

    This object will be instantiated from calling
    :meth:`~github3.issues.issue.Issue.events` which calls
    https://developer.github.com/v3/issues/events/#list-events-for-an-issue

    See also: http://developer.github.com/v3/issues/events

    This object has the following attributes:

    .. attribute:: actor

        A :class:`~github3.users.ShortUser` representing the user who
        generated this event.

    .. attribute:: commit_id

        The string SHA of a commit that referenced the parent issue. If there
        was no commit referencing this issue, then this will be ``None``.

    .. attribute:: commit_url

        The URL to retrieve commit information from the API for the commit
        that references the parent issue. If there was no commit, this will be
        ``None``.

    .. attribute:: created_at

        A :class:`~datetime.datetime` object representing the date and time
        this event occurred.

    .. attribute:: event

        The issue-specific action that generated this event. Some examples
        are:

        - closed
        - reopened
        - subscribed
        - merged
        - referenced
        - mentioned
        - assigned

        See `this list of events`_ for a full listing.

    .. attribute:: id

        The unique identifier for this event.

    .. _this list of events:
        https://developer.github.com/v3/issues/events/#events-1
    """

    def _update_attributes(self, event):
        self._api = event['url']
        self.actor = users.ShortUser(event['actor'], self)
        self.commit_id = event['commit_id']
        self.commit_url = event['commit_url']
        self.created_at = event['created_at']
        self.event = event['event']
        self.id = event['id']
        self._uniq = self.commit_id

    def _repr(self):
        return '<Issue Event [{0} by {1}]>'.format(
            self.event, self.actor
        )


class RepositoryIssueEvent(IssueEvent):
    """Representation of an issue event on the repository level.

    This object will be instantiated from calling
    :meth:`~github3.repos.repo.Repository.issue_events` or
    :meth:`~github3.repos.repo.ShortRepository.issue_events`which call
    https://developer.github.com/v3/issues/events/#list-events-for-a-repository

    See also: http://developer.github.com/v3/issues/events

    This object has all of the attributes of
    :class:`~github3.issues.event.IssueEvent` and the following:

    .. attribute:: issue

        A :class:`~github3.issues.issue.ShortIssue` representing the issue
        where this event originated from.

    """

    def _update_attributes(self, event):
        super(RepositoryIssueEvent, self)._update_attributes(event)
        from . import issue
        self.issue = issue.ShortIssue(event['issue'], self)

    def _repr(self):
        return '<Repository Issue Event on #{} [{} by {}]>'.format(
            self.issue.number, self.event, self.actor.login
        )
