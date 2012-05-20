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
from .issue import Issue


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
            gist = Gist(loads(response.content), self._session)

        return gist

    def gist(self, id_num):
        """Gets the gist using the specified id number."""
        url = '/'.join([self._github_url, 'gists', str(id_num)])
        req = self._session.get(url)
        gist = None
        if req.status_code == 200:
            gist = Gist(loads(req.content), self._session)

        return gist

    def gists(self, username=None):
        """If no username is specified, GET /gists, otherwise GET
        /users/:username/gists"""
        _url = [self._github_url]
        if username:
            _url.extend(['users', username, 'gists'])
        else:
            _url.append('gists')
        url = '/'.join(_url)

        req = self._session.get(url)
        data = loads(req.content)

        gists = []
        for d in data:
            gists.append(Gist(d, self._session))

        return gists

    def issue(self, owner, repository, number):
        url = '/'.join([self._github_url, 'repos', owner, repository, 'issues',
            str(number)])
        req = self._session.get(url)
        issue = None
        if req.status_code == 200:
            issue = Issue(loads(req.content), self._session)

        return issue

    def issues(self, owner=None, repository=None):
        _url = [self._github_url]
        if owner and repository:
            _url.extend(['repos', owner, repository, 'issues'])
        else:
            _url.append('issues')
        url = '/'.join(_url)

        issues = []
        req = self._session.get(url)
        if req.status_code == 200:
            jissues = loads(req.content)
            for jissue in jissues:
                issues.append(Issue(jissue, self._session))

        return issues

    def login(self, username, password):
        """Logs the user into GitHub for protected API calls."""
        self._session.auth = (username, password)
