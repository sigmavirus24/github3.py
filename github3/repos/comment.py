# -*- coding: utf-8 -*-
"""
github3.repos.comment
=====================

This module contains the RepoComment class

"""
from github3.decorators import requires_auth
from github3.models import BaseComment
from github3.users import User


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
    def __init__(self, comment, session=None):
        super(RepoComment, self).__init__(comment, session)
        #: Commit id on which the comment was made.
        self.commit_id = comment.get('commit_id')
        #: URL of the comment on GitHub.
        self.html_url = comment.get('html_url')
        #: The line number where the comment is located.
        self.line = comment.get('line')
        #: The path to the file where the comment was made.
        self.path = comment.get('path')
        #: The position in the diff where the comment was made.
        self.position = comment.get('position')
        #: datetime object representing when the comment was updated.
        self.updated_at = comment.get('updated_at')
        if self.updated_at:
            self.updated_at = self._strptime(self.updated_at)
        #: Login of the user who left the comment.
        self.user = None
        if comment.get('user'):
            self.user = User(comment.get('user'), self)

    def __repr__(self):
        return '<Repository Comment [{0}/{1}]>'.format(
            self.commit_id[:7], self.user.login or ''
        )

    def _update_(self, comment):
        super(RepoComment, self)._update_(comment)
        self.__init__(comment, self._session)

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
            self._update_(json)
            return True
        return False
