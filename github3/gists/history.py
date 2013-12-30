# -*- coding: utf-8 -*-
"""
github3.gists.history
---------------------

Module containing the logic for the GistHistory object.

"""

from github3.models import GitHubCore
from github3.users import User


class GistHistory(GitHubCore):

    """Thisobject represents one version (or revision) of a gist.

    Two history instances can be checked like so::

        h1 == h2
        h1 != h2

    And is equivalent to::

        h1.version == h2.version
        h1.version != h2.version

    """

    def __init__(self, history, session=None):
        super(GistHistory, self).__init__(history, session)
        self._api = history.get('url', '')

        #: SHA of the commit associated with this version
        self.version = history.get('version', '')

        #: user who made these changes
        self.user = User(history.get('user') or {}, session)

        #: dict containing the change status; see also: deletions, additions,
        #: total
        self.change_status = history.get('change_status', {})

        #: number of additions made
        self.additions = self.change_status.get('additions', 0)

        #: number of deletions made
        self.deletions = self.change_status.get('deletions', 0)

        #: total number of changes made
        self.total = self.change_status.get('total', 0)

        #: datetime representation of when the commit was made
        self.committed_at = self._strptime(history.get('committed_at'))

    def __repr__(self):
        return '<Gist History [{0}]>'.format(self.version)

    def get_gist(self):
        """Retrieve the gist at this version.

        :returns: :class:`Gist <github3.gists.gist.Gist>`

        """
        from github3.gists.gist import Gist
        json = self._json(self._get(self._api), 200)
        return Gist(json, self)
