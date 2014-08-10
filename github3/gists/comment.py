# -*- coding: utf-8 -*-
"""
github3.gists.comment
---------------------

Module containing the logic for a GistComment

"""
from __future__ import unicode_literals

from github3.models import BaseComment
from github3.users import User


class GistComment(BaseComment):

    """This object represents a comment on a gist.

    Two comment instances can be checked like so::

        c1 == c2
        c1 != c2

    And is equivalent to::

        c1.id == c2.id
        c1.id != c2.id

    See also: http://developer.github.com/v3/gists/comments/

    """

    def __init__(self, comment, session=None):
        super(GistComment, self).__init__(comment, session)

        #: :class:`User <github3.users.User>` who made the comment
        #: Unless it is not associated with an account
        self.user = None
        if comment.get('user'):
            self.user = User(comment.get('user'), self)  # (No coverage)

    def _repr(self):
        return '<Gist Comment [{0}]>'.format(self.user.login)
