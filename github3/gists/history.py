# -*- coding: utf-8 -*-
"""
github3.gists.history
---------------------

Module containing the logic for the GistHistory object.

"""
from __future__ import unicode_literals

from .. import users
from ..models import GitHubCore


class GistHistory(GitHubCore):

    """Thisobject represents one version (or revision) of a gist.

    Two history instances can be checked like so::

        h1 == h2
        h1 != h2

    And is equivalent to::

        h1.version == h2.version
        h1.version != h2.version

    """

    def _update_attributes(self, history):
        self._api = self._get_attribute(history, 'url')

        #: SHA of the commit associated with this version
        self.version = self._get_attribute(history, 'version')

        #: user who made these changes
        self.user = self._class_attribute(
            history, 'user', users.ShortUser, self,
        )

        #: dict containing the change status; see also: deletions, additions,
        #: total
        self.change_status = self._get_attribute(history, 'change_status', {})

        #: number of additions made
        self.additions = self._get_attribute(self.change_status, 'additions')

        #: number of deletions made
        self.deletions = self._get_attribute(self.change_status, 'deletions')

        #: total number of changes made
        self.total = self._get_attribute(self.change_status, 'total')

        #: datetime representation of when the commit was made
        self.committed_at = self._strptime_attribute(history, 'committed_at')

    def _repr(self):
        return '<Gist History [{0}]>'.format(self.version)

    def get_gist(self):
        """Retrieve the gist at this version.

        :returns: :class:`Gist <github3.gists.gist.Gist>`

        """
        from .gist import Gist
        json = self._json(self._get(self._api), 200)
        return self._instance_or_null(Gist, json)
