# -*- coding: utf-8 -*-
"""
github3.repos.status
====================

This module contains the Status object for GitHub's commit status API

"""
from __future__ import unicode_literals

from .. import users

from ..models import GitHubCore


class Status(GitHubCore):
    """The :class:`Status <Status>` object.

    This represents information from the Repo Status API.

    See also: http://developer.github.com/v3/repos/statuses/
    """

    def _update_attributes(self, status):
        #: A string label to differentiate this status from the status of
        #: other systems
        self.context = self._get_attribute(status, 'context')

        #: datetime object representing the creation of the status object
        self.created_at = self._strptime_attribute(status, 'created_at')

        #: :class:`User <github3.users.User>` who created the object
        self.creator = self._class_attribute(
            status, 'creator', users.ShortUser
        )

        #: Short description of the Status
        self.description = self._get_attribute(status, 'description')

        #: GitHub ID for the status object
        self.id = self._get_attribute(status, 'id')

        #: State of the status, e.g., 'success', 'pending', 'failed', 'error'
        self.state = self._get_attribute(status, 'state')

        #: URL to view more information about the status
        self.target_url = self._get_attribute(status, 'target_url')

        #: datetime object representing the last time the status was updated
        self.updated_at = self._strptime_attribute(status, 'updated_at')

    def _repr(self):
        return '<Status [{s.id}:{s.state}]>'.format(s=self)


class CombinedStatus(GitHubCore):
    """The :class:`CombinedStatus <CombinedStatus>` object.

    This represents combined information from the Repo Status API.

    See also: http://developer.github.com/v3/repos/statuses/
    """

    def _update_attributes(self, combined_status):
        #: State of the combined status, e.g., 'success', 'pending', 'failure'
        self.state = self._get_attribute(combined_status, 'state')

        #: ref's SHA
        self.sha = self._get_attribute(combined_status, 'sha')

        #: Total count of sub-statuses
        self.total_count = self._get_attribute(combined_status, 'total_count')

        #: List of :class:`Status <github3.repos.status.Status>`
        #: objects.
        statuses = self._get_attribute(combined_status, 'statuses', [])
        self.statuses = [Status(s) for s in statuses]

        from . import Repository
        #: Repository the combined status belongs too.
        self.repository = self._class_attribute(
            combined_status, 'repository', Repository, self
        )

        #: commit URL
        self.commit_url = self._get_attribute(combined_status, 'commit_url')

    def _repr(self):
        f = '<CombinedStatus [{s.state}:{s.total_count} sub-statuses]>'
        return f.format(s=self)
