"""
github3.git
===========

This module contains all the classes relating to Git Data.

"""

from base64 import b64decode
from json import dumps
from .models import GitHubObject, GitHubCore, BaseCommit
from .users import User


class Blob(GitHubObject):
    """The :class:`Blob <Blob>` object."""
    def __init__(self, blob):
        super(Blob, self).__init__(blob)
        self._api = blob.get('url')
        self._content = blob.get('content').encode()
        self._enc = blob.get('encoding')
        if self._enc == 'base64':
            self._decoded = b64decode(self._content)
        else:
            self._decoded = self._content
        self._size = blob.get('size')
        self._sha = blob.get('sha')

    def __repr__(self):
        return '<Blob [{0:.10}]>'.format(self._sha)

    @property
    def content(self):
        """Raw content of the blob."""
        return self._content

    @property
    def decoded(self):
        """Decoded content of the blob."""
        return self._decoded

    @property
    def encoding(self):
        """Encoding of the raw content."""
        return self._enc

    @property
    def sha(self):
        """SHA1 of the blob"""
        return self._sha

    @property
    def size(self):
        """Size of the blob in bytes"""
        return self._size


class GitData(GitHubCore):
    """The :class:`GitData <GitData>` object. This isn't directly returned to
    the user (developer) ever. This is used to prevent duplication of some
    common items among other Git Data objects.
    """
    def __init__(self, data, session=None):
        super(GitData, self).__init__(data, session)
        self._sha = data.get('sha')
        self._api = data.get('url')

    def __repr__(self):
        return '<github3-gitdata at 0x{0:x}>'.format(id(self))

    @property
    def sha(self):
        """SHA of the object"""
        return self._sha


class Commit(BaseCommit):
    """The :class:`Commit <Commit>` object. This represents a commit made in a
    repository.
    """
    def __init__(self, commit, session=None):
        super(Commit, self).__init__(commit, session)

        self._author = ''
        self._author_name = ''
        if commit.get('author') and len(commit.get('author')) > 3:
            # User object
            # Typically there should be 5 keys, but more than 3 should
            # be a sufficient test
            self._author = User(commit.get('author'), None)
            self._author_name = self._author.login
        elif commit.get('author'):  # Not a User object
            self._author = type('Author', (object, ), commit.get('author'))
            self._author_name = self._author.name

        self._committer = ''
        if commit.get('committer'):
            if len(commit.get('committer')) > 3:
                self._committer = User(commit.get('committer'), None)
            else:
                self._committer = type('Committer', (object, ),
                        commit.get('committer'))

        self._tree = None
        if commit.get('tree'):
            self._tree = Tree(commit.get('tree'), self._session)

    def __repr__(self):
        return '<Commit [{0}:{1}]>'.format(self._author_name, self._sha)

    @property
    def author(self):
        """:class:`User <github3.user.User>` who authored the commit."""
        return self._author

    @property
    def committer(self):
        """:class:`User <github3.user.User>` who committed the commit."""
        return self._committer

    @property
    def tree(self):
        """:class:`Tree <Tree>` the commit belongs to."""
        return self._tree


class Reference(GitHubCore):
    """The :class:`Reference <Reference>` object. This represents a reference
    created on a repository.
    """
    def __init__(self, ref, session=None):
        super(Reference, self).__init__(ref, session)
        self._update_(ref)

    def __repr__(self):
        return '<Reference [{0}]>'.format(self._ref)

    def _update_(self, ref):
        self._ref = ref.get('ref')
        self._api = ref.get('url')
        self._obj = GitObject(ref.get('object'))

    @GitHubCore.requires_auth
    def delete(self):
        """Delete this reference.

        :returns: bool
        """
        return self._boolean(self._delete(self._api), 204, 404)

    @property
    def object(self):
        """:class:`GitObject <GitObject>` the reference points to"""
        return self._obj

    @property
    def ref(self):
        """The reference path, e.g., refs/heads/sc/featureA"""
        return self._ref

    @GitHubCore.requires_auth
    def update(self, sha, force=False):
        """Update this reference.

        :param sha: (required), sha of the reference
        :type sha: str
        :param force: (optional), force the update or not
        :type force: bool
        :returns: bool
        """
        data = dumps({'sha': sha, 'force': force})
        json = self._json(self._patch(self._api, data), 200)
        if json:
            self._update_(json)
            return True
        return False


class GitObject(GitData):
    """The :class:`GitObject <GitObject>` object."""
    def __init__(self, obj):
        super(GitObject, self).__init__(obj, None)
        self._type = obj.get('type')

    def __repr__(self):
        return '<Git Object [{0}]>'.format(self._sha)

    @property
    def type(self):
        """The type of object."""
        return self._type


class Tag(GitData):
    def __init__(self, tag):
        super(Tag, self).__init__(tag, None)
        self._tag = tag.get('tag')
        self._msg = tag.get('message')
        self._tagger = None
        if tag.get('tagger'):
            self._tagger = type('Tagger', (object, ), tag.get('tagger'))
        self._obj = GitObject(tag.get('object'))

    def __repr__(self):
        return '<Tag [{0}]>'.format(self._tag)

    @property
    def message(self):
        return self._msg

    @property
    def object(self):
        return self._obj

    @property
    def tag(self):
        return self._tag

    @property
    def tagger(self):
        return self._tagger


class Tree(GitData):
    """The :class:`Tree <Tree>` object."""
    def __init__(self, tree, session=None):
        super(Tree, self).__init__(tree, session)
        self._tree = [Hash(t) for t in tree.get('tree', [])]

    def __repr__(self):
        return '<Tree [{0}]>'.format(self._sha)

    def recurse(self):
        """Recurse into the tree.

        :returns: :class:`Tree <Tree>`
        """
        url = self._api + '?recursive=1'
        json = self._json(self._get(url), 200)
        return Tree(json, self._session) if json else None

    @property
    def tree(self):
        """list of :class:`Hash <Hash>` objects"""
        return self._tree


class Hash(GitHubObject):
    """The :class:`Hash <Hash>` object."""
    def __init__(self, info):
        super(Hash, self).__init__(info)
        self._path = info.get('path')
        self._mode = info.get('mode')
        self._type = info.get('type')
        self._size = info.get('size')
        self._sha = info.get('sha')
        self._url = info.get('url')

    @property
    def mode(self):
        """File mode"""
        return self._mode

    @property
    def path(self):
        """Path to file"""
        return self._path

    @property
    def sha(self):
        """SHA of the hash"""
        return self._sha

    @property
    def size(self):
        """Size of hash"""
        return self._size

    @property
    def type(self):
        """Type of hash, e.g., blob"""
        return self._type

    @property
    def url(self):
        """URL of this object in the GitHub API"""
        return self._url
