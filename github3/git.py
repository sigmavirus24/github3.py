# -*- coding: utf-8 -*-
"""
This module contains all the classes relating to Git Data.

See also: http://developer.github.com/v3/git/
"""
from __future__ import unicode_literals
import base64
import warnings

from json import dumps

from . import models
from .decorators import requires_auth


class Blob(models.GitHubCore):
    """This object provides an interface to the API representation of a blob.

    See also: http://developer.github.com/v3/git/blobs/

    .. versionchanged:: 1.0.0

       - The :attr:`content` is no longer forcibly coerced to bytes.
       - The :attr:`decoded` is deprecated in favor of :meth:`decode_content`.

    This object has the following atributes

    .. attribute:: content

        The raw content of the blob. This may be base64 encoded text. Use
        :meth:`decode_content` to receive the non-encoded text.

    .. attribute:: encoding

        The encoding that GitHub reports for this blob's content.

    .. attribute:: size

        The size of this blob's content in bytes.

    .. attribute:: sha

        The SHA1 of this blob's content.
    """

    def _update_attributes(self, blob):
        self._api = blob['url']
        self.content = blob['content']
        self.encoding = blob['encoding']
        self.size = blob['size']
        self.sha = blob['sha']

    def _repr(self):
        return '<Blob [{0:.10}]>'.format(self.sha)

    @property
    def decoded(self):
        """Compatibility shim for the deprecated attribute."""
        warnings.warn('The decoded attribute is deprecated. Use decode_content'
                      ' instead.', DeprecationWarning)
        return self.decode_content()

    def decode_content(self):
        """Return the unencoded content of this blob.

        If the content is base64 encoded, this will properly decode it.
        Otherwise, it will return the content as returned by the API.

        :returns:
            Decoded content as text
        :rtype:
            unicode
        """
        if self.encoding == 'base64' and self.content:
            return base64.b64decode(
                self.content.encode('utf-8')
            ).decode('utf-8')
        return self.content


class Commit(models.GitHubCore):
    """This represents a commit as returned by the git API.

    This is distinct from :class:`~github3.repos.commit.RepoCommit`.
    Primarily this object represents the commit data stored by git and
    it has no relationship to the repository on GitHub.

    See also: http://developer.github.com/v3/git/commits/

    This object has the following attributes:

    .. attribute:: author

        This is a dictionary with at least the name and email of the author
        of this commit as well as the date it was authored.

    .. attribute:: committer

        This is a dictionary with at least the name and email of the committer
        of this commit as well as the date it was committed.

    .. attribute:: html_url

        The URL to view this commit in a browser.

    .. attribute:: message

        The commit message that describes the changes as written by the author
        and committer.

    .. attribute:: parents

        The list of commits that are the parents of this commit. This may be
        empty if this is the initial commit, or it may have several if it is
        the result of an octopus merge. Each parent is represented as a
        dictionary with the API URL and SHA1.

    .. attribute:: sha

        The unique SHA1 which identifies this commit.

    .. attribute:: tree

        The git tree object this commit points to.

    .. attribute:: verification

        The GPG verification data about this commit. See
        https://developer.github.com/v3/git/commits/#commit-signature-verification
        for more information.
    """

    def _update_attributes(self, commit):
        self._api = commit['url']
        self.author = commit['author']
        if self.author.get('name'):
            self._author_name = self.author['name']
        self.committer = commit['committer']
        if self.committer:
            self._commit_name = self.committer.get('name')
        self.html_url = commit['html_url']
        self.message = commit['message']
        self.parents = commit['parents']
        self.sha = commit['sha']
        if not self.sha:
            i = self._api.rfind('/')
            self.sha = self._api[i + 1:]
        self._uniq = self.sha
        self.tree = CommitTree(commit['tree'], self)
        self.verification = commit['verification']

    def _repr(self):
        return '<Commit [{0}]>'.format(self.sha)


class Reference(models.GitHubCore):
    """The :class:`Reference <Reference>` object.

    This represents a reference created on a repository.

    See also: http://developer.github.com/v3/git/refs/

    """

    def _update_attributes(self, ref):
        self._api = ref['url']

        #: The reference path, e.g., refs/heads/sc/featureA
        self.ref = ref['ref']

        #: :class:`GitObject <GitObject>` the reference points to
        self.object = GitObject(ref['object'], self)

    def _repr(self):
        return '<Reference [{0}]>'.format(self.ref)

    @requires_auth
    def delete(self):
        """Delete this reference.

        :returns: bool

        """
        return self._boolean(self._delete(self._api), 204, 404)

    @requires_auth
    def update(self, sha, force=False):
        """Update this reference.

        :param str sha: (required), sha of the reference
        :param bool force: (optional), force the update or not
        :returns: bool

        """
        data = {'sha': sha, 'force': force}
        json = self._json(self._patch(self._api, data=dumps(data)), 200)
        if json:
            self._update_attributes(json)
            return True
        return False


class GitObject(models.GitHubCore):
    """The :class:`GitObject <GitObject>` object."""

    def _update_attributes(self, obj):
        self.sha = self._get_attribute(obj, 'sha')
        self._api = self._get_attribute(obj, 'url')
        self.type = self._get_attribute(obj, 'type')

    def _repr(self):
        return '<Git Object [{0}]>'.format(self.sha)


class Tag(models.GitHubCore):
    """The :class:`Tag <Tag>` object.

    See also: http://developer.github.com/v3/git/tags/

    """

    def _update_attributes(self, tag):
        self.sha = self._get_attribute(tag, 'sha')
        self._api = self._get_attribute(tag, 'url')

        #: String of the tag
        self.tag = tag['tag']

        #: Commit message for the tag
        self.message = tag['message']

        #: dict containing the name and email of the person
        self.tagger = tag['tagger']

        #: :class:`GitObject <GitObject>` for the tag
        self.object = GitObject(tag['object'], self)

    def _repr(self):
        return '<Tag [{0}]>'.format(self.tag)


class CommitTree(models.GitHubCore):
    """The :class:`CommitTree <CommitTree>` object.

    Represents the tree data found in a commit object

    """

    def _update_attributes(self, tree):
        self._api = tree['url']
        self.sha = tree['sha']

    def _repr(self):
        return '<CommitTree [{0}]>'.format(self.sha)

    def to_tree(self):
        """Retrieve a full Tree object for this CommitTree."""
        json = self._json(self._get(self._api), 200)
        return self._instance_or_null(Tree, json)

    refresh = to_tree


class Tree(models.GitHubCore):
    """The :class:`Tree <Tree>` object.

    See also: http://developer.github.com/v3/git/trees/

    """

    def _update_attributes(self, tree):
        self.sha = self._get_attribute(tree, 'sha')
        self._api = self._get_attribute(tree, 'url')

        #: list of :class:`Hash <Hash>` objects
        self.tree = tree['tree']
        if self.tree:
            self.tree = [Hash(t, self) for t in self.tree]

    def _repr(self):
        return '<Tree [{0}]>'.format(self.sha)

    def __eq__(self, other):
        return self.as_dict() == other.as_dict()

    def __ne__(self, other):
        return self.as_dict() != other.as_dict()

    def recurse(self):
        """Recurse into the tree.

        :returns: :class:`Tree <Tree>`
        """
        json = self._json(self._get(self._api, params={'recursive': '1'}),
                          200)
        return self._instance_or_null(Tree, json)


class Hash(models.GitHubCore):
    """The :class:`Hash <Hash>` object.

    See also: http://developer.github.com/v3/git/trees/#create-a-tree

    """

    def _update_attributes(self, info):
        #: Path to file
        self.path = info['path']

        #: File mode
        self.mode = info['mode']

        #: Type of hash, e.g., blob
        self.type = info['type']

        #: Size of hash
        # Size is not set if the type is a tree
        if self.type != 'tree':
            self.size = info['size']

        #: SHA of the hash
        self.sha = info['sha']

        #: URL of this object in the GitHub API
        self.url = info['url']

    def _repr(self):
        return '<Hash [{0}]>'.format(self.sha)
