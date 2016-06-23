# -*- coding: utf-8 -*-
"""
github3.empty
=============

This module contains everything relating to the Empty class.

"""


class Empty(object):

    """Class to indicate something wasn't returned by the API.

    The :class:`Empty <Empty>` class indicates that the attribute requested
    was not found in the json returned by the API. The Empty class is declared
    in every GitHubCore subclass using GitHubCore.Empty.

    A model's field can be checked for Empty like so::

        # type(user) == github3.users.User
        user.owner_private_repos is not user.Empty

    And that is equivalent to::

        from github3.empty import Empty
        user.owner_private_repos is not Empty

    """
