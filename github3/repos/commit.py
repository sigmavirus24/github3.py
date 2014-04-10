# -*- coding: utf-8 -*-
"""
github3.repos.commit
====================

This module contains the RepoCommit class alone

"""
from __future__ import unicode_literals

from github3.git import Commit
from github3.models import BaseCommit
from github3.users import User


class RepoCommit(BaseCommit):
    """The :class:`RepoCommit <RepoCommit>` object. This represents a commit as
    viewed by a :class:`Repository`. This is different from a Commit object
    returned from the git data section.

    Two commit instances can be checked like so::

        c1 == c2
        c1 != c2

    And is equivalent to::

        c1.sha == c2.sha
        c1.sha != c2.sha

    """
    def __init__(self, commit, session=None):
        super(RepoCommit, self).__init__(commit, session)
        #: :class:`User <github3.users.User>` who authored the commit.
        self.author = commit.get('author')
        if self.author:
            self.author = User(self.author, self._session)
        #: :class:`User <github3.users.User>` who committed the commit.
        self.committer = commit.get('committer')
        if self.committer:
            self.committer = User(self.committer, self._session)
        #: :class:`Commit <github3.git.Commit>`.
        self.commit = commit.get('commit')
        if self.commit:
            self.commit = Commit(self.commit, self._session)

        self.sha = commit.get('sha')
        #: The number of additions made in the commit.
        self.additions = 0
        #: The number of deletions made in the commit.
        self.deletions = 0
        #: Total number of changes in the files.
        self.total = 0
        if commit.get('stats'):
            self.additions = commit['stats'].get('additions')
            self.deletions = commit['stats'].get('deletions')
            self.total = commit['stats'].get('total')

        #: The files that were modified by this commit.
        self.files = commit.get('files', [])

        self._uniq = self.sha

    def _repr(self):
        return '<Repository Commit [{0}]>'.format(self.sha[:7])

    def diff(self):
        """Return the diff"""
        resp = self._get(self._api,
                         headers={'Accept': 'application/vnd.github.diff'})
        return resp.content if self._boolean(resp, 200, 404) else None

    def patch(self):
        """Return the patch"""
        resp = self._get(self._api,
                         headers={'Accept': 'application/vnd.github.patch'})
        return resp.content if self._boolean(resp, 200, 404) else None
