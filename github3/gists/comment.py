# -*- coding: utf-8 -*-
"""
github3.gists.comment
---------------------

Module containing the logic for a GistComment

"""
from __future__ import unicode_literals

from .. import users
from ..models import BaseComment


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

    def _update_attributes(self, comment):
        self._api = self._get_attribute(comment, 'url')
        #: :class:`User <github3.users.User>` who made the comment
        #: Unless it is not associated with an account
        self.user = self._class_attribute(
            comment, 'user', users.ShortUser, self,
        )

    def _repr(self):
        return '<Gist Comment [{0}]>'.format(self.user.login)
