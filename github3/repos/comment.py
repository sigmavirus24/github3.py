# -*- coding: utf-8 -*-
"""
github3.repos.comment
=====================

This module contains the RepoComment class

"""
from __future__ import unicode_literals

from .. import users

from ..decorators import requires_auth
from ..models import BaseComment


class RepoComment(BaseComment):
    """The :class:`RepoComment <RepoComment>` object. This stores the
    information about a comment on a file in a repository.

    Two comment instances can be checked like so::

        c1 == c2
        c1 != c2

    And is equivalent to::

        c1.id == c2.id
        c1.id != c2.id

    """
    def _update_attributes(self, comment):
        super(RepoComment, self)._update_attributes(comment)

        #: Commit id on which the comment was made.
        self.commit_id = self._get_attribute(comment, 'commit_id')

        #: URL of the comment on GitHub.
        self.html_url = self._get_attribute(comment, 'html_url')

        #: The line number where the comment is located.
        self.line = self._get_attribute(comment, 'line')

        #: The path to the file where the comment was made.
        self.path = self._get_attribute(comment, 'path')

        #: The position in the diff where the comment was made.
        self.position = self._get_attribute(comment, 'position')

        #: datetime object representing when the comment was updated.
        self.updated_at = self._strptime_attribute(comment, 'updated_at')

        #: Login of the user who left the comment.
        self.user = self._class_attribute(
            comment, 'user', users.ShortUser, self
        )

    def _repr(self):
        return '<Repository Comment [{0}/{1}]>'.format(
            self.commit_id[:7], self.user.login or ''
        )

    @requires_auth
    def update(self, body):
        """Update this comment.

        :param str body: (required)
        :returns: bool
        """
        json = None
        if body:
            json = self._json(self._post(self._api, data={'body': body}), 200)

        if json:
            self._update_attributes(json)
            return True
        return False
