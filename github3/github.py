"""
github3.github
==============

This module contains the main GitHub session object.

"""

from requests import session
from json import dumps
from .compat import loads
from .models import GitHubCore
from .gist import Gist

class GitHub(GitHubCore):
    """Stores all the session information."""
    def __init__(self):
        super(GitHub, self).__init__()
        self._session = session()
        # Only accept JSON responses
        self._session.headers.update({'Accept': 'application/json'})
        # Only accept UTF-8 encoded data
        self._session.headers.update({'Accept-Charset': 'utf-8'})

    def __repr__(self):
        return '<github3-session at 0x%x>' % id(self)

    def login(self, username, password):
        """Logs the user into GitHub for protected API calls."""
        self._session.auth = (username, password)

    def gist(self, id_num):
        """Gets the gist using the specified id number."""
        url = '/'.join([self._github_url, 'gists', str(id_num)])
        req = self._session.get(url)
        data = loads(req.content)
        _gist = Gist(data)
        _gist._session = self._session
        return _gist

    def gists(self, username=None):
        """If no username is specified, GET /gists, otherwise GET 
        /users/:username/gists"""
        if username:
            url = '/'.join([self._github_url, 'users', username,
                'gists'])
        else:
            url = '/'.join([self._github_url, 'gists'])

        req = self._session.get(url)
        data = loads(req.content)

        _gists = []
        for d in data:
            _gist = Gist(d)
            _gist._session = self._session
            _gists.append(_gist)

        return _gists

    def create_gist(self, description, files, public=True):
        """Create a new gist.

        If no login was provided, it will be anonymous.
        """
        new_gist = {'description': description, 'public': public,
                'files': files}

        _url = '/'.join([self._github_url, 'gists'])
        response = self._session.post(_url, dumps(new_gist))

        gist = None
        if response.status_code == 201:
            gist = Gist(loads(response.content))
        
        return gist
