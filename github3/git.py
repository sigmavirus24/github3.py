"""
github3.git
===========

This module contains all the classes relating to Git Data.

"""

from json import dumps
from .user import User


class Commit(object):
    def __init__(self, commit):
        super(Commit, self).__init__()
        self._sha = commit.get('sha')
        self._api_url = commit.get('url')
        self._author = User(commit.get('author'), None)
        self._committer = User(commit.get('committer'), None)
        self._msg = commit.get('message')
        self._parents = []
        for parent in commit.get('parents'):
            api = parent.pop('url')
            parent['_api_url'] = api
            self._parents.append(type('Parent', (object, ), parent))

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
    def sha(self):
        return self._sha
