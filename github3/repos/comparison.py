# -*- coding: utf-8 -*-
"""
github3.repos.comparison
========================

This module contains the Comparison object for comparing two commits via the
GitHub API.

"""
from __future__ import unicode_literals

from ..models import GitHubCore
from .commit import RepoCommit


class Comparison(GitHubCore):
    """The :class:`Comparison <Comparison>` object. This encapsulates the
    information returned by GitHub comparing two commit objects in a
    repository.

    Two comparison instances can be checked like so::

        c1 == c2
        c1 != c2

    And is equivalent to::

        c1.commits == c2.commits
        c1.commits != c2.commits

    See also:
    http://developer.github.com/v3/repos/commits/#compare-two-commits
    """

    def _update_attributes(self, compare):
        self._api = self._get_attribute(compare, 'url')

        #: URL to view the comparison at GitHub
        self.html_url = self._get_attribute(compare, 'html_url')

        #: Permanent link to this comparison.
        self.permalink_url = self._get_attribute(compare, 'permalink_url')

        #: URL to see the diff between the two commits.
        self.diff_url = self._get_attribute(compare, 'diff_url')

        #: Patch URL at GitHub for the comparison.
        self.patch_url = self._get_attribute(compare, 'patch_url')

        #: :class:`RepoCommit <github3.repos.commit.RepoCommit>` object
        #: representing the base of comparison.
        self.base_commit = self._class_attribute(
            compare, 'base_commit', RepoCommit, None
        )

        #: Behind or ahead.
        self.status = self._get_attribute(compare, 'status')

        #: Number of commits ahead by.
        self.ahead_by = self._get_attribute(compare, 'ahead_by')

        #: Number of commits behind by.
        self.behind_by = self._get_attribute(compare, 'behind_by')

        #: Number of commits difference in the comparison.
        self.total_commits = self._get_attribute(compare, 'total_commits')

        #: List of :class:`RepoCommit <github3.repos.commit.RepoCommit>`
        #: objects.
        self.commits = self._get_attribute(compare, 'commits', [])
        if self.commits:
            self.commits = [RepoCommit(com) for com in self.commits]

        #: List of dicts describing the files modified.
        self.files = self._get_attribute(compare, 'files', [])

        self._uniq = self.commits

    def _repr(self):
        return '<Comparison of {0} commits>'.format(self.total_commits)

    def diff(self):
        """Retrieve the diff for this comparison.

        :returns: the diff as a bytes object
        :rtype: bytes
        """
        resp = self._get(self._api,
                         headers={'Accept': 'application/vnd.github.diff'})
        return resp.content if self._boolean(resp, 200, 404) else b''

    def patch(self):
        """Retrieve the patch formatted diff for this commit.

        :returns: the patch as a bytes object
        :rtype: bytes
        """
        resp = self._get(self._api,
                         headers={'Accept': 'application/vnd.github.patch'})
        return resp.content if self._boolean(resp, 200, 404) else b''
