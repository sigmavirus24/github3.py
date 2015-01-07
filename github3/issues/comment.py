# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..models import BaseComment
from ..users import User


class IssueComment(BaseComment):
    """The :class:`IssueComment <IssueComment>` object. This structures and
    handles the comments on issues specifically.

    Two comment instances can be checked like so::

        c1 == c2
        c1 != c2

    And is equivalent to::

        c1.id == c2.id
        c1.id != c2.id

    See also: http://developer.github.com/v3/issues/comments/
    """
    def __init__(self, comment, session=None):
        super(IssueComment, self).__init__(comment, session)

        user = comment.get('user')
        #: :class:`User <github3.users.User>` who made the comment
        self.user = User(user, self) if user else None

        #: Issue url (not a template)
        self.issue_url = comment.get('issue_url')

    def _repr(self):
        return '<Issue Comment [{0}]>'.format(self.user.login)
