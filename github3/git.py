"""
github3.git
===========

This module contains all the classes relating to Git Data.

"""

from base64 import b64decode
from json import dumps
from github3.models import GitHubObject, GitHubCore, BaseCommit
from github3.users import User
from github3.decorators import requires_auth


class Blob(GitHubObject):
    """The :class:`Blob <Blob>` object."""
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
    """
    def __init__(self, commit, session=None):
        super(Commit, self).__init__(commit, session)

        #: :class:`User <github3.users.User>` who authored the commit.
        self.author = commit.get('author')
        self._author_name = commit.get('author')
        if commit.get('author') and len(commit.get('author')) > 3:
            # User object
            # Typically there should be 5 keys, but more than 3 should
            # be a sufficient test
            self.author = User(commit.get('author'), None)
        elif commit.get('author'):  # Not a User object
            self.author = type('Author', (object, ), commit.get('author'))

        #: :class:`User <github3.user.User>` who committed the commit.
        self.committer = None
        if commit.get('committer'):
            self.committer = User(commit.get('committer'), None)

        #: :class:`Tree <Tree>` the commit belongs to.
        self.tree = None
        if commit.get('tree'):
            self.tree = Tree(commit.get('tree'), self._session)

    def __repr__(self):
        return '<Commit [{0}:{1}]>'.format(self.author.name, self.sha)


class Reference(GitHubCore):
    """The :class:`Reference <Reference>` object. This represents a reference
    created on a repository.
    """
    def __init__(self, ref, session=None):
        super(Reference, self).__init__(ref, session)
        self._api = ref.get('url', '')
        #: The reference path, e.g., refs/heads/sc/featureA
        self.ref = ref.get('ref')
        #: :class:`GitObject <GitObject>` the reference points to
        self.object = GitObject(ref.get('object'))

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

        :param sha: (required), sha of the reference
        :type sha: str
        :param force: (optional), force the update or not
        :type force: bool
        :returns: bool
        """
        data = dumps({'sha': sha, 'force': force})
        json = self._json(self._patch(self._api, data=data), 200)
        if json:
            self._update_(json)
            return True
        return False  # (No coverage)


class GitObject(GitData):
    """The :class:`GitObject <GitObject>` object."""
    def __init__(self, obj):
        super(GitObject, self).__init__(obj, None)
        #: The type of object.
        self.type = obj.get('type')

    def __repr__(self):
        return '<Git Object [{0}]>'.format(self.sha)


class Tag(GitData):
    def __init__(self, tag):
        super(Tag, self).__init__(tag, None)
        #: String of the tag
        self.tag = tag.get('tag')
        #: Commit message for the tag
        self.message = tag.get('message')
        #: dict containing the name and email of the person
        self.tagger = tag.get('tagger')
        #: :class:`GitObject <GitObject>` for the tag
        self.object = GitObject(tag.get('object'))

    def __repr__(self):
        return '<Tag [{0}]>'.format(self.tag)


class Tree(GitData):
    """The :class:`Tree <Tree>` object."""
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
    """The :class:`Hash <Hash>` object."""
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
