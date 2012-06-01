"""
github3.git
===========

This module contains all the classes relating to Git Data.

"""

from base64 import b64decode
from json import dumps
from .models import GitHubCore
from .user import User


class Blob(object):
    def __init__(self, blob):
        super(Blob, self).__init__()
        self._content = blob.get('content')
        self._enc = blob.get('encoding')
        if self._enc == 'base64':
            self._decoded = b64decode(self._content)
        else:
            self._decoded = self._content

    def __repr__(self):
        return '<Blob [%0.10s]>' % self._decoded

    @property
    def content(self):
        return self._content

    @property
    def decoded(self):
        return self._decoded

    @property
    def encoding(self):
        return self._enc

class GitData(GitHubCore):
    def __init__(self, data, session):
        super(GitData, self).__init__(session)
        self._sha = data.get('sha')
        self._api = data.get('url')

    def __repr__(self):
        return '<github3-gitdata at 0x%x>' % id(self)

    @property
    def sha(self):
        return self._sha


class Commit(GitData):
    def __init__(self, commit, session):
        super(Commit, self).__init__(commit, session)

        self._author = ''
        if len(commit.get('author')) > 3:  # User object
            # Typically there should be 5 keys, but more than 3 should 
            # be a sufficient test
            self._author = User(commit.get('author'), None)
        elif commit.get('author'):  # Not a User object
            self._author = type('Author', (object, ), commit.get('author'))

        self._committer = ''
        if commit.get('committer'):
            if len(commit.get('committer')) > 3:
                self._committer = User(commit.get('committer'), None)
            else:
                self._committer = type('Committer', (object, ),
                        commit.get('committer'))
        self._msg = commit.get('message')
        self._parents = []
        for parent in commit.get('parents'):
            api = parent.pop('url')
            parent['_api'] = api
            self._parents.append(type('Parent', (object, ), parent))

        self._tree = None
        if commit.get('tree'):
            self._tree = Tree(commit.get('tree'), self._session)

    def __repr__(self):
        return '<Commit [%s:%s]>' % (self._author.login, self._sha)

    @property
    def author(self):
        return self._author

    @property
    def committer(self):
        return self._committer

    @property
    def message(self):
        return self._msg

    @property
    def parents(self):
        return self._parents

    @property
    def tree(self):
        return self._tree


class Reference(GitHubCore):
    def __init__(self, ref, session):
        super(Reference, self).__init__(session)
        self._update_(ref)

    def __repr__(self):
        return '<Reference [%s]>' % self._ref

    def _update_(self, ref):
        self._ref = ref.get('ref')
        self._api = ref.get('url')
        self._obj = GitObject(ref.get('object'))

    def delete(self):
        return self._delete(self._api)

    @property
    def object(self):
        return self._obj

    @property
    def ref(self):
        return self._ref

    def update(self, sha, force=False):
        data = dumps({'sha': sha, 'force': force})
        json = self._patch(self._api, data)
        if json:
            self._update_(json)
            return True
        return False


class GitObject(GitData):
    def __init__(self, obj):
        super(GitObject, self).__init__(obj, None)
        self._type = obj.get('type')

    def __repr__(self):
        return '<Git Object [%s]>' % self._sha

    @property
    def type(self):
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
        return '<Tag [%s]>' % self._tag

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
    def __init__(self, tree, session):
        super(Tree, self).__init__(tree, session)
        self._tree = []
        if tree.get('tree'):
            for t in tree.get('tree'):
                self._tree.append(Hash(t))

    def __repr__(self):
        return '<Tree [%s]>' % self._sha

    def recurse(self):
        url = self._api + '?recursive=1'
        json = self._get(url)
        return Tree(json, self._session) if json else None

    @property
    def tree(self):
        return self._tree


class Hash(object):
    def __init__(self, info):
        super(Hash, self).__init__()
        self._path = info.get('path')
        self._mode = info.get('mode')
        self._type = info.get('type')
        self._size = info.get('size')
        self._sha = info.get('sha')
        self._url = info.get('url')

    @property
    def mode(self):
        return self._mode

    @property
    def path(self):
        return self._path

    @property
    def sha(self):
        return self._sha

    @property
    def size(self):
        return self._size

    @property
    def type(self):
        return self._type

    @property
    def url(self):
        return self._url
