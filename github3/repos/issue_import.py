# -*- coding: utf-8 -*-
from ..models import GitHubCore


"""
github3.repos.issue_import
==========================

This module contains the ImportedIssue object for Github's import issue API

"""


class ImportedIssue(GitHubCore):
    """
    The :class:`ImportedIssue <ImportedIssue>` object. This represents
    information from the Import Issue API.

    See also: https://gist.github.com/jonmagic/5282384165e0f86ef105
    """

    IMPORT_CUSTOM_HEADERS = {
        'Accept': 'application/vnd.github.golden-comet-preview+json'
    }

    def _update_attributes(self, issue):
        self.id = self._get_attribute(issue, 'id')

        self.status = self._get_attribute(issue, 'status')

        self.url = self._get_attribute(issue, 'url')

        # Since created_at and updated_at returns slightly different format
        # we can't use self._strptime
        # For example, repo correctly returns '2015-04-15T03:40:51Z'
        # For ImportedIssue, the format is '2016-01-14T10:57:56-08:00'
        self.created_at = self._get_attribute(issue, 'created_at')
        self.updated_at = self._get_attribute(issue, 'updated_at')
        self.import_issues_url = self._get_attribute(
            issue, 'import_issues_url'
        )
        self.repository_url = self._get_attribute(issue, 'repository_url')
