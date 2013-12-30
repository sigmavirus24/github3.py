# -*- coding: utf-8 -*-
"""
github3.git
===========

This module contains all the classes relating to Git Data.

See also: http://developer.github.com/v3/git/
"""

from json import dumps
from base64 import b64decode
from github3.models import GitHubObject, GitHubCore, BaseCommit
from github3.users import User
from github3.decorators import requires_auth


class Blob(GitHubObject):

    """The :class:`Blob <Blob>` object.

    See also: http://developer.github.com/v3/git/blobs/

    """

    def __init__(self, blob):
        super(Blob, self).__init__(blob)
        self._api = blob.get('url', '')

        #: Raw content of the blob.
        self.content = blob.get('content').encode()

        #: Encoding of the raw content.
        self.encoding = blob.get('encoding')

        #: Decoded content of the blob.
        self.decoded = self.content
        if self.encoding == 'base64':
            self.decoded = b64decode(self.content)

        #: Size of the blob in bytes
        self.size = blob.get('size')
        #: SHA1 of the blob
        self.sha = blob.get('sha')

    def __repr__(self):
        return '<Blob [{0:.10}]>'.format(self.sha)


class GitData(GitHubCore):

    """The :class:`GitData <GitData>` object. This isn't directly returned to
    the user (developer) ever. This is used to prevent duplication of some
    common items among other Git Data objects.

    """

    def __init__(self, data, session=None):
        super(GitData, self).__init__(data, session)
        #: SHA of the object
        self.sha = data.get('sha')
        self._api = data.get('url', '')


class Commit(BaseCommit):

    """The :class:`Commit <Commit>` object. This represents a commit made in a
    repository.

    See also: http://developer.github.com/v3/git/commits/

    """

    def __init__(self, commit, session=None):
        super(Commit, self).__init__(commit, session)

        #: dict containing at least the name, email and date the commit was
        #  created
        self.author = commit.get('author', {}) or {}
        # If GH returns nil/None then make sure author is a dict
        self._author_name = self.author.get('name', '')

        #: dict containing similar information to the author attribute
        self.committer = commit.get('committer', {}) or {}
        # blank the data if GH returns no data

        self._commit_name = self.committer.get('name', '')

        #: :class:`Tree <Tree>` the commit belongs to.
        self.tree = None
        if commit.get('tree'):
            self.tree = Tree(commit.get('tree'), self._session)

    def __repr__(self):
        return '<Commit [{0}:{1}]>'.format(self._author_name, self.sha)

    def author_as_User(self):
        """Attempt to return the author attribute as a
        :class:`User <github3.users.User>`. No guarantees are made about the
        validity of this object, i.e., having a login or created_at object.

        """
        return User(self.author, self._session)

    def committer_as_User(self):
        """Attempt to return the committer attribute as a
        :class:`User <github3.users.User>` object. No guarantees are made
        about the validity of this object.

        """
        return User(self.committer, self._session)


class Reference(GitHubCore):

    """The :class:`Reference <Reference>` object. This represents a reference
    created on a repository.

    See also: http://developer.github.com/v3/git/refs/

    """

    def __init__(self, ref, session=None):
        super(Reference, self).__init__(ref, session)
        self._api = ref.get('url', '')
        #: The reference path, e.g., refs/heads/sc/featureA
        self.ref = ref.get('ref')
        #: :class:`GitObject <GitObject>` the reference points to
        self.object = GitObject(ref.get('object', {}))

    def __repr__(self):
        return '<Reference [{0}]>'.format(self.ref)

    def _update_(self, ref):
        self.__init__(ref, self._session)

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
            self._update_(json)
            return True
        return False


class GitObject(GitData):

    """The :class:`GitObject <GitObject>` object."""

    def __init__(self, obj):
        super(GitObject, self).__init__(obj, None)
        #: The type of object.
        self.type = obj.get('type')

    def __repr__(self):
        return '<Git Object [{0}]>'.format(self.sha)


class Tag(GitData):

    """The :class:`Tag <Tag>` object.

    See also: http://developer.github.com/v3/git/tags/

    """

    def __init__(self, tag):
        super(Tag, self).__init__(tag, None)
        #: String of the tag
        self.tag = tag.get('tag')
        #: Commit message for the tag
        self.message = tag.get('message')
        #: dict containing the name and email of the person
        self.tagger = tag.get('tagger')
        #: :class:`GitObject <GitObject>` for the tag
        self.object = GitObject(tag.get('object', {}))

    def __repr__(self):
        return '<Tag [{0}]>'.format(self.tag)


class Tree(GitData):

    """The :class:`Tree <Tree>` object.

    See also: http://developer.github.com/v3/git/trees/

    """

    def __init__(self, tree, session=None):
        super(Tree, self).__init__(tree, session)
        #: list of :class:`Hash <Hash>` objects
        self.tree = [Hash(t) for t in tree.get('tree', [])]

    def __repr__(self):
        return '<Tree [{0}]>'.format(self.sha)

    def recurse(self):
        """Recurse into the tree.

        :returns: :class:`Tree <Tree>`
        """
        json = self._json(self._get(self._api, params={'recursive': '1'}),
                          200)
        return Tree(json, self._session) if json else None


class Hash(GitHubObject):

    """The :class:`Hash <Hash>` object.

    See also: http://developer.github.com/v3/git/trees/#create-a-tree

    """

    def __init__(self, info):
        super(Hash, self).__init__(info)
        #: Path to file
        self.path = info.get('path')
        #: File mode
        self.mode = info.get('mode')
        #: Type of hash, e.g., blob
        self.type = info.get('type')
        #: Size of hash
        self.size = info.get('size')
        #: SHA of the hash
        self.sha = info.get('sha')
        #: URL of this object in the GitHub API
        self.url = info.get('url')

    def __repr__(self):
        return '<Hash [{0}]>'.format(self.sha)
