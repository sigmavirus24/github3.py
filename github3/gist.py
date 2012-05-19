"""
gist.py
=======

Module which contains all the gist related material.
"""

from datetime import datetime
from json import dumps
from .compat import loads
from .models import GitHubCore
from .user import User

class GistFile(object):
    def __init__(self, attributes):
        super(GistFile, self).__init__()

        self._raw = attributes.get('raw_url')
        self._name = attributes.get('filename')
        self._language = attributes.get('language')
        self._size = attributes.get('size')
        self._content = attributes.get('content')

    def __repr__(self):
        return '<Gist File [%s]>' % self._name

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def name(self):
        return self._name

    @property
    def lang(self):
        return self._language

    @property
    def raw_url(self):
        return self._raw

    @property
    def size(self):
        return self._size


class Gist(GitHubCore):
    def __init__(self, data):
        super(Gist, self).__init__()

        self._update_(data)

    def __repr__(self):
        return '<Gist [%s]>' % self._id

    def _update_(self, data):
        # The gist identifier
        self._id = data.get('id')
        self._desc = data.get('description')

        # e.g. https://api.github.com/gists/1
        self._api_url = data.get('url')
        # e.g. https://gist.github.com/1
        self._url = data.get('html_url')
        self._public = data.get('public')
        # a list of all the forks of that gist
        self._forks = data.get('forks', [])
        # e.g. git://gist.github.com/1.git
        self._pull = data.get('git_pull_url')
        # e.g. git@gist.github.com/1.git
        self._push = data.get('git_push_url')
        # date the gist was created
        self._created = datetime.strptime(data.get('created_at'),
                self._time_format)
        self._updated = datetime.strptime(data.get('updated_at'),
                self._time_format)
        self._user = User(data.get('user'))

        # Create a list of files in the gist
        self._files = []
        for file in data['files']:
            self._files.append(GistFile(data['files'][file]))

    @property
    def created(self):
        return self._created

    def delete(self):
        """Delete this gist."""
        resp = self._session.delete(self._api_url)
        if resp.status_code == 204:
            return True
        return False

    @property
    def description(self):
        return self._desc

    def edit(self, **kwargs):
        """Edit this gist. 

        :param kwargs: Should be either (or both) description or files.
        """
        resp = self._session.patch(self._api_url, dumps(kwargs))
        if resp.status_code == 200:
            self._update_(loads(resp.content))
            return True
        return False

    @property
    def files(self):
        return self._files

    def fork(self):
        url = '/'.join([self._api_url, 'fork'])
        resp = self._session.post(url)
        if resp.status_code == 201:
            return Gist(loads(resp.content))
        return False

    @property
    def forks(self):
        return self._forks

    def get(self):
        """GET /gists/:id"""
        resp = self._session.get(self._api_url)
        if resp.status_code == 200:
            self._update_(loads(resp.content))
            return True
        return False

    @property
    def git_pull(self):
        return self._pull

    @property
    def git_push(self):
        return self._push

    @property
    def html_url(self):
        return self._url

    def is_public(self):
        return self._public

    def is_starred(self):
        url = '/'.join([self._api_url, 'star'])
        resp = self._session.get(url)
        if resp.status_code == 204:
            return True
        return False

    def star(self):
        """Star this gist."""
        url = '/'.join([self._api_url, 'star'])
        resp = self._session.put(url)
        if resp.status_code == 204:
            return True
        return False

    def unstar(self):
        """Un-star this gist."""
        url = '/'.join([self._api_url, 'star'])
        resp = self._session.delete(url)
        if resp.status_code == 204:
            return True
        return False

    @property
    def updated(self):
        return self._updated

    @property
    def user(self):
        return self._user
