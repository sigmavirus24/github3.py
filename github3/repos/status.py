# -*- coding: utf-8 -*-
"""
github3.repos.status
====================

This module contains the Status object for GitHub's commit status API

"""
from __future__ import unicode_literals

from ..models import GitHubCore
from ..users import User


class Status(GitHubCore):
    """The :class:`Status <Status>` object. This represents information from
    the Repo Status API.

    See also: http://developer.github.com/v3/repos/statuses/
    """
    def _update_attributes(self, status):
        #: A string label to differentiate this status from the status of
        #: other systems
        self.context = status.get('context')
        #: datetime object representing the creation of the status object
        self.created_at = self._strptime(status.get('created_at'))
        #: :class:`User <github3.users.User>` who created the object
        if status.get('creator'):
            self.creator = User(status.get('creator'))
        #: Short description of the Status
        self.description = status.get('description')
        #: GitHub ID for the status object
        self.id = status.get('id')
        #: State of the status, e.g., 'success', 'pending', 'failed', 'error'
        self.state = status.get('state')
        #: URL to view more information about the status
        self.target_url = status.get('target_url')
        #: datetime object representing the last time the status was updated
        self.updated_at = self._strptime(status.get('updated_at'))

    def _repr(self):
        return '<Status [{s.id}:{s.state}]>'.format(s=self)

class CombinedStatus(GitHubCore):
    """The :class:`CombinedStatus <CombinedStatus>` object. This represents combined
    information from the Repo Status API.

    See also: http://developer.github.com/v3/repos/statuses/
    """
    def _update_attributes(self, combined_status):
        #: State of the combined status, e.g., 'success', 'pending', 'failure'
        self.state = combined_status.get('state')
        #: Total count of sub-statuses
        self.total_count = combined_status.get('total_count')
        #: List of :class:`Status <github3.repos.status.Status>`
        #: objects.
        self.statuses = [Status(status) for status in combined_status.get('statuses')]

    def _repr(self):
        return '<CombinedStatus [{s.state}:{s.total_count} sub-statuses]>'.format(s=self)
