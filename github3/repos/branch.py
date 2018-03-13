# -*- coding: utf-8 -*-
"""Implementation of a branch on a repository."""
from __future__ import unicode_literals

from json import dumps

from . import commit
from .. import models


class _Branch(models.GitHubCore):
    """A representation of a branch on a repository.

    See also https://developer.github.com/v3/repos/branches/

    This object has the following attributes:
    """

    # The Accept header will likely be removable once the feature is out of
    # preview mode. See: http://git.io/v4O1e
    PREVIEW_HEADERS = {'Accept': 'application/vnd.github.loki-preview+json'}

    class_name = 'Repository Branch'

    def _update_attributes(self, branch):
        self.commit = commit.MiniCommit(branch['commit'], self)
        self.name = branch['name']

    def _repr(self):
        return '<{0} [{1}]>'.format(self.class_name, self.name)

    def latest_sha(self, differs_from=''):
        """Check if SHA-1 is the same as remote branch.

        See: https://git.io/vaqIw

        :param str differs_from:
            (optional), sha to compare against
        :returns:
            string of the SHA or None
        """
        # If-None-Match returns 200 instead of 304 value does not have quotes
        headers = {
            'Accept': 'application/vnd.github.v3.sha',
            'If-None-Match': '"{0}"'.format(differs_from)
        }
        base = self._api.split('/branches', 1)[0]
        url = self._build_url('commits', self.name, base_url=base)
        resp = self._get(url, headers=headers)
        if self._boolean(resp, 200, 304):
            return resp.content
        return None

    def protect(self, enforcement=None, status_checks=None):
        """Enable force push protection and configure status check enforcement.

        See: http://git.io/v4Gvu

        :param str enforcement:
            (optional), Specifies the enforcement level of the status checks.
            Must be one of 'off', 'non_admins', or 'everyone'. Use `None` or
            omit to use the already associated value.
        :param list status_checks:
            (optional), An list of strings naming status checks that must pass
            before merging. Use `None` or omit to use the already associated
            value.
        :returns:
            True if successful, False otherwise
        :rtype:
            bool
        """
        previous_values = None
        if self.protection:
            previous_values = self.protection['required_status_checks']
        if enforcement is None and previous_values:
            enforcement = previous_values['enforcement_level']
        if status_checks is None and previous_values:
            status_checks = previous_values['contexts']

        edit = {'protection': {'enabled': True, 'required_status_checks': {
            'enforcement_level': enforcement, 'contexts': status_checks}}}
        json = self._json(self._patch(self._api, data=dumps(edit),
                                      headers=self.PREVIEW_HEADERS), 200)
        self._update_attributes(json)
        return True

    def unprotect(self):
        """Disable force push protection on this branch."""
        edit = {'protection': {'enabled': False}}
        json = self._json(self._patch(self._api, data=dumps(edit),
                                      headers=self.PREVIEW_HEADERS), 200)
        self._update_attributes(json)
        return True


class Branch(_Branch):
    """The representation of a branch returned in a collection.

    GitHub's API returns different amounts of information about repositories
    based upon how that information is retrieved. This object exists to
    represent the limited amount of information returned for a specific
    branch in a collection. For example, you would receive this class when
    calling :meth:`~github3.repos.repo.Repository.branches`. To provide a
    clear distinction between the types of branches, github3.py uses different
    classes with different sets of attributes.

    This object has the same attributes as a
    :class:`~github3.repos.branch.ShortBranch` as well as the following:

    .. attribute:: links

        The dictionary of URLs returned by the API as ``_links``.

    .. attribute:: protected

        A boolean attribute that describes whether this branch is protected or
        not.

    .. attribute:: protection

        A dictionary with details about the protection configuration of this
        branch.

    .. attribute:: protection_url

        The URL to access and manage details about this branch's protection.
    """

    class_name = 'Repository Branch'

    def _update_attributes(self, branch):
        super(Branch, self)._update_attributes(branch)
        self.commit = commit.ShortCommit(branch['commit'], self)
        #: Returns '_links' attribute.
        self.links = branch['_links']
        #: Provides the branch's protection status.
        self.protected = branch['protected']
        self.protection = branch['protection']
        self.protection_url = branch['protection_url']
        if self.links and 'self' in self.links:
            self._api = self.links['self']
        elif isinstance(self.commit, commit.ShortCommit):
            # Branches obtained via `repo.branches` don't have links.
            base = self.commit.url.split('/commit', 1)[0]
            self._api = self._build_url('branches', self.name, base_url=base)


class ShortBranch(_Branch):
    """The representation of a branch returned in a collection.

    GitHub's API returns different amounts of information about repositories
    based upon how that information is retrieved. This object exists to
    represent the limited amount of information returned for a specific
    branch in a collection. For example, you would receive this class when
    calling :meth:`~github3.repos.repo.Repository.branches`. To provide a
    clear distinction between the types of branches, github3.py uses different
    classes with different sets of attributes.

    This object has the following attributes:

    .. attribute:: commit

        A :class:`~github3.repos.commit.MiniCommit` representation of the
        newest commit on this branch with the associated repository metadata.

    .. attribute:: name

        The name of this branch.
    """

    class_name = 'Short Repository Branch'
    _refresh_to = Branch
