# -*- coding: utf-8 -*-
"""Module containing the GistHistory object."""
from __future__ import unicode_literals

from .. import users
from ..models import GitHubCore


class GistHistory(GitHubCore):
    """This object represents one version (or revision) of a gist.

    The GitHub API returns the following attributes:

    .. attribute:: url

        The URL to the revision of the gist retrievable through the API.

    .. attribute:: version

        The commit ID of the revision of the gist.

    .. attribute:: user

        The :class:`~github3.users.ShortUser` representation of the user who
        owns this gist.

    .. attribute:: committed_at

        The date and time of the revision's commit.

    .. attribute:: change_status

        A dictionary with the number of deletions, additions, and total
        changes to the gist.

    For convenience, github3.py also exposes the following attributes from the
    :attr:`change_status`:

    .. attribute:: additions

        The number of additions to the gist compared to the previous revision.

    .. attribute:: deletions

        The number of deletions from the gist compared to the previous
        revision.

    .. attribute:: totoal

        The total number of changes to the gist compared to the previous
        revision.
    """

    def _update_attributes(self, history):
        self.url = self._api = history['url']

        #: SHA of the commit associated with this version
        self.version = history['version']

        #: user who made these changes
        self.user = users.ShortUser(history['user'], self)

        #: dict containing the change status; see also: deletions, additions,
        #: total
        self.change_status = history['change_status']

        #: number of additions made
        self.additions = self.change_status['additions']

        #: number of deletions made
        self.deletions = self.change_status['deletions']

        #: total number of changes made
        self.total = self.change_status['total']

        #: datetime representation of when the commit was made
        self.committed_at = self._strptime(history['committed_at'])

    def _repr(self):
        return '<Gist History [{0}]>'.format(self.version)

    def gist(self):
        """Retrieve the gist at this version.

        :returns: the gist at this point in history or ``None``
        :rtype: :class:`Gist <github3.gists.gist.Gist>`
        """
        from .gist import Gist
        json = self._json(self._get(self._api), 200)
        return self._instance_or_null(Gist, json)
