"""
gist.py
=======

Module which contains all the gist related material.
"""

from datetime import datetime
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

        # The gist identifier
        self._id = data['id']
        self._desc = data['description']

        # e.g. https://api.github.com/gists/1
        self._api_url = data['url']
        # e.g. https://gist.github.com/1
        self._url = data['html_url']
        self._public = data['public']
        # a list of all the forks of that gist
        self._forks = data.get('forks', [])
        # e.g. git://gist.github.com/1.git
        self._pull = data['git_pull_url']
        # e.g. git@gist.github.com/1.git
        self._push = data['git_push_url']
        # date the gist was created
        self._created = datetime.strptime(data['created_at'], 
                self._time_format)
        self._updated = datetime.strptime(data['updated_at'],
                self._time_format)
        self._user = User(data['user'])

        # Create a list of files in the gist
        self._files = []
        for file in data['files']:
            self._files.append(GistFile(data['files'][file]))

    def __repr__(self):
        return '<Gist [%s]>' % self._id

    @property
    def created(self):
        return self._created

    @property
    def description(self):
        return self._desc

    @property
    def forks(self):
        return self._forks

    def get(self):
        """GET /gists/:id"""
        req = self._session.get(self._api_url)

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

    @property
    def updated(self):
        return self._updated

    @property
    def user(self):
        return self._user

    @property
    def files(self):
        return self._files
