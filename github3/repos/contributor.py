# -*- coding: utf-8 -*-
"""
github3.repo.contributors
=============

This module contains a subclass of User with contribution-specific attributes.

"""
from __future__ import unicode_literals

from github3.users import User


class Contributor(User):

    """The :class:`Contributor <Contributor>` object.

    Two contributor instances can be checked like so::

        c1 == c2
        c1 != c2

    And is equivalent to::

        c1.id == c2.id
        c1.id != c2.id

    See also: https://developer.github.com/v3/repos/#list-contributors

    """
    def __init__(self, contributor, session=None):
        super(Contributor, self).__init__(contributor, session)

        #: Number of contributions
        self.contributions = contributor.get('contributions')
