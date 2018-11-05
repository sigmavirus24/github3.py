# -*- coding: utf-8 -*-
"""This module contains the Comparison object."""
from __future__ import unicode_literals

from . import commit
from .. import models


class Comparison(models.GitHubCore):
    """A representation of a comparison between two or more commit objects.

    See also:
    http://developer.github.com/v3/repos/commits/#compare-two-commits

    This object has the following attributes::

    .. attribute:: ahead_by

        The number of commits between the head and base commit.

    .. attribute:: base_commit

        A :class:`~github3.repos.commit.ShortCommit` representing the base
        commit in this comparison.

    .. attribute:: behind_by

        The number of commits the head commit is behind the base.

    .. attribute:: commits

        A list of :class:`~github3.repos.commit.ShortCommit` objects
        representing the commits in the comparison.

    .. attribute:: diff_url

        The URL to retrieve the diff between the head and base commits.

    .. attribute:: files

        A list of dictionaries describing each of the modified files in the
        comparison.

    .. attribute:: html_url

        The URL to view the comparison in a browser.

    .. attribute:: patch_url

        The URL to retrieve the patch-formatted diff of this comparison.

    .. attribute:: permalink_url

        The permanent URL to retrieve this comparison.

    .. attribute:: status

        Whether the head commit is ahead or behind of base.

    .. attribute:: total_commits

        The total number of commits difference.
    """

    def _update_attributes(self, compare):
        self._api = compare["url"]
        self.ahead_by = compare["ahead_by"]
        self.base_commit = commit.ShortCommit(compare["base_commit"], self)
        self.behind_by = compare["behind_by"]
        self.commits = compare["commits"]
        if self.commits:
            self.commits = [
                commit.ShortCommit(com, self) for com in self.commits
            ]
        self.diff_url = compare["diff_url"]
        self.files = compare["files"]
        self.html_url = compare["html_url"]
        self.patch_url = compare["patch_url"]
        self.permalink_url = compare["permalink_url"]
        self.status = compare["status"]
        self.total_commits = compare["total_commits"]
        self._uniq = self.commits

    def _repr(self):
        return "<Comparison of {0} commits>".format(self.total_commits)

    def diff(self):
        """Retrieve the diff for this comparison.

        :returns:
            the diff as a bytes object
        :rtype:
            bytes
        """
        resp = self._get(
            self._api, headers={"Accept": "application/vnd.github.diff"}
        )
        return resp.content if self._boolean(resp, 200, 404) else b""

    def patch(self):
        """Retrieve the patch formatted diff for this commit.

        :returns:
            the patch as a bytes object
        :rtype:
            bytes
        """
        resp = self._get(
            self._api, headers={"Accept": "application/vnd.github.patch"}
        )
        return resp.content if self._boolean(resp, 200, 404) else b""
