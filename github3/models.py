# -*- coding: utf-8 -*-
"""
github3.models
==============

This module provides the basic models used in github3.py

"""

from json import dumps
from requests.compat import urlparse
from github3.decorators import requires_auth
from github3.session import GitHubSession
from datetime import datetime
from logging import getLogger

__timeformat__ = '%Y-%m-%dT%H:%M:%SZ'
__logs__ = getLogger(__package__)


class GitHubObject(object):
    """The :class:`GitHubObject <GitHubObject>` object. A basic class to be
    subclassed by GitHubCore and other classes that would otherwise subclass
    object."""
    def __init__(self, json):
        super(GitHubObject, self).__init__()
        if json is not None:
            self.etag = json.pop('ETag', None)
            self.last_modified = json.pop('Last-Modified', None)
        self._json_data = json
        self._uniq = json.get('url', None)

    def to_json(self):
        """Return the json representing this object."""
        return self._json_data

    def _strptime(self, time_str):
        """Converts an ISO 8601 formatted string into a datetime object."""
        if time_str:
            return datetime.strptime(time_str, __timeformat__)
        return None

    @classmethod
    def from_json(cls, json):
        """Return an instance of ``cls`` formed from ``json``."""
        return cls(json)

    def __eq__(self, other):
        return self._uniq == other._uniq

    def __ne__(self, other):
        return self._uniq != other._uniq

    def __hash__(self):
        return hash(self._uniq)


class GitHubCore(GitHubObject):
    """The :class:`GitHubCore <GitHubCore>` object. This class provides some
    basic attributes to other classes that are very useful to have.
    """
    def __init__(self, json, session=None):
        super(GitHubCore, self).__init__(json)
        if hasattr(session, '_session'):
            # i.e. session is actually a GitHub object
            session = session._session
        elif session is None:
            session = GitHubSession()
        self._session = session

        # set a sane default
        self._github_url = 'https://api.github.com'

    def __repr__(self):
        return '<github3-core at 0x{0:x}>'.format(id(self))

    def _remove_none(self, data):
        if not data:
            return
        for (k, v) in list(data.items()):
            if v is None:
                del(data[k])

    def _json(self, response, status_code):
        ret = None
        if self._boolean(response, status_code, 404) and response.content:
            __logs__.info('Attempting to get JSON information from a Response '
                          'with status code %d expecting %d',
                          response.status_code, status_code)
            ret = response.json()
            headers = response.headers
            if ((headers.get('Last-Modified') or headers.get('ETag')) and
                    isinstance(ret, dict)):
                ret['Last-Modified'] = response.headers.get(
                    'Last-Modified', ''
                )
                ret['ETag'] = response.headers.get('ETag', '')
        __logs__.info('JSON was %sreturned', 'not ' if ret is None else '')
        return ret

    def _boolean(self, response, true_code, false_code):
        if response is not None:
            status_code = response.status_code
            if status_code == true_code:
                return True
            if status_code != false_code and status_code >= 400:
                raise GitHubError(response)
        return False

    def _delete(self, url, **kwargs):
        __logs__.debug('DELETE %s with %s', url, kwargs)
        return self._session.delete(url, **kwargs)

    def _get(self, url, **kwargs):
        __logs__.debug('GET %s with %s', url, kwargs)
        return self._session.get(url, **kwargs)

    def _patch(self, url, **kwargs):
        __logs__.debug('PATCH %s with %s', url, kwargs)
        return self._session.patch(url, **kwargs)

    def _post(self, url, data=None, json=True, **kwargs):
        if json:
            data = dumps(data) if data is not None else data
        elif 'headers' in kwargs:
            # Override the Content-Type header
            kwargs['headers'] = {
                'Content-Type': None
                }.update(kwargs['headers'])
        __logs__.debug('POST %s with %s, %s', url, data, kwargs)
        return self._session.post(url, data, **kwargs)

    def _put(self, url, **kwargs):
        __logs__.debug('PUT %s with %s', url, kwargs)
        return self._session.put(url, **kwargs)

    def _build_url(self, *args, **kwargs):
        """Builds a new API url from scratch."""
        return self._session.build_url(*args, **kwargs)

    @property
    def _api(self):
        return "{0.scheme}://{0.netloc}{0.path}".format(self._uri)

    @_api.setter
    def _api(self, uri):
        self._uri = urlparse(uri)

    def _iter(self, count, url, cls, params=None, etag=None):
        """Generic iterator for this project.

        :param int count: How many items to return.
        :param int url: First URL to start with
        :param class cls: cls to return an object of
        :param params dict: (optional) Parameters for the request
        :param str etag: (optional), ETag from the last call
        """
        from github3.structs import GitHubIterator
        return GitHubIterator(count, url, cls, self, params, etag)

    @property
    def ratelimit_remaining(self):
        """Number of requests before GitHub imposes a ratelimit.

        :returns: int
        """
        json = self._json(self._get(self._github_url + '/rate_limit'), 200)
        core = json.get('resources', {}).get('core', {})
        self._remaining = core.get('remaining', 0)
        return self._remaining

    def refresh(self, conditional=False):
        """Re-retrieve the information for this object and returns the
        refreshed instance.

        :param bool conditional: If True, then we will search for a stored
            header ('Last-Modified', or 'ETag') on the object and send that
            as described in the `Conditional Requests`_ section of the docs
        :returns: self

        The reasoning for the return value is the following example: ::

            repos = [r.refresh() for r in g.iter_repos('kennethreitz')]

        Without the return value, that would be an array of ``None``'s and you
        would otherwise have to do: ::

            repos = [r for i in g.iter_repos('kennethreitz')]
            [r.refresh() for r in repos]

        Which is really an anti-pattern.

        .. versionchanged:: 0.5

        .. _Conditional Requests:
            http://developer.github.com/v3/#conditional-requests
        """
        headers = {}
        if conditional:
            if self.last_modified:
                headers['If-Modified-Since'] = self.last_modified
            elif self.etag:
                headers['If-None-Match'] = self.etag

        headers = headers or None
        json = self._json(self._get(self._api, headers=headers), 200)
        if json is not None:
            self.__init__(json, self._session)
        return self


class BaseComment(GitHubCore):
    """The :class:`BaseComment <BaseComment>` object. A basic class for Gist,
    Issue and Pull Request Comments."""
    def __init__(self, comment, session):
        super(BaseComment, self).__init__(comment, session)
        #: Unique ID of the comment.
        self.id = comment.get('id')
        #: Body of the comment. (As written by the commenter)
        self.body = comment.get('body')
        #: Body of the comment formatted as plain-text. (Stripped of markdown,
        #  etc.)
        self.body_text = comment.get('body_text')
        #: Body of the comment formatted as html.
        self.body_html = comment.get('body_html')
        #: datetime object representing when the comment was created.
        self.created_at = self._strptime(comment.get('created_at'))
        #: datetime object representing when the comment was updated.
        self.updated_at = self._strptime(comment.get('updated_at'))

        self._api = comment.get('url', '')
        self.links = comment.get('_links')
        #: The url of this comment at GitHub
        self.html_url = ''
        #: The url of the pull request, if it exists
        self.pull_request_url = ''
        if self.links:
            self.html_url = self.links.get('html')
            self.pull_request_url = self.links.get('pull_request')

    def _update_(self, comment):
        self.__init__(comment, self._session)

    @requires_auth
    def delete(self):
        """Delete this comment.

        :returns: bool
        """
        return self._boolean(self._delete(self._api), 204, 404)

    @requires_auth
    def edit(self, body):
        """Edit this comment.

        :param str body: (required), new body of the comment, Markdown
            formatted
        :returns: bool
        """
        if body:
            json = self._json(self._patch(self._api,
                              data=dumps({'body': body})), 200)
            if json:
                self._update_(json)
                return True
        return False


class BaseCommit(GitHubCore):
    """The :class:`BaseCommit <BaseCommit>` object. This serves as the base for
    the various types of commit objects returned by the API.
    """
    def __init__(self, commit, session):
        super(BaseCommit, self).__init__(commit, session)
        self._api = commit.get('url', '')
        #: SHA of this commit.
        self.sha = commit.get('sha')
        #: Commit message
        self.message = commit.get('message')
        #: List of parents to this commit.
        self.parents = commit.get('parents', [])
        #: URL to view the commit on GitHub
        self.html_url = commit.get('html_url', '')
        if not self.sha:
            i = self._api.rfind('/')
            self.sha = self._api[i + 1:]

        self._uniq = self.sha


class BaseAccount(GitHubCore):
    """The :class:`BaseAccount <BaseAccount>` object. This is used to do the
    heavy lifting for :class:`Organization <github3.orgs.Organization>` and
    :class:`User <github3.users.User>` objects.
    """
    def __init__(self, acct, session):
        super(BaseAccount, self).__init__(acct, session)
        #: Tells you what type of account this is
        self.type = None
        if acct.get('type'):
            self.type = acct.get('type')
        self._api = acct.get('url', '')

        #: URL of the avatar at gravatar
        self.avatar_url = acct.get('avatar_url', '')
        #: URL of the blog
        self.blog = acct.get('blog', '')
        #: Name of the company
        self.company = acct.get('company', '')

        #: datetime object representing the date the account was created
        self.created_at = None
        if acct.get('created_at'):
            self.created_at = self._strptime(acct.get('created_at'))

        #: E-mail address of the user/org
        self.email = acct.get('email')

        ## The number of people following this acct
        #: Number of followers
        self.followers = acct.get('followers', 0)

        ## The number of people this acct follows
        #: Number of people the user is following
        self.following = acct.get('following', 0)

        #: Unique ID of the account
        self.id = acct.get('id', 0)
        #: Location of the user/org
        self.location = acct.get('location', '')
        #: login name of the user/org
        self.login = acct.get('login', '')

        ## e.g. first_name last_name
        #: Real name of the user/org
        self.name = acct.get('name') or ''
        self.name = self.name.encode('utf-8')

        ## The number of public_repos
        #: Number of public repos owned by the user/org
        self.public_repos = acct.get('public_repos', 0)

        ## e.g. https://github.com/self._login
        #: URL of the user/org's profile
        self.html_url = acct.get('html_url', '')

        #: Markdown formatted biography
        self.bio = acct.get('bio')

    def __repr__(self):
        return '<{s.type} [{s.login}:{s.name}]>'.format(s=self)

    def _update_(self, acct):
        self.__init__(acct, self._session)


class GitHubError(Exception):
    def __init__(self, resp):
        super(GitHubError, self).__init__(resp)
        #: Response code that triggered the error
        self.response = resp
        self.code = resp.status_code
        self.errors = []
        try:
            error = resp.json()
            #: Message associated with the error
            self.msg = error.get('message')
            #: List of errors provided by GitHub
            if error.get('errors'):
                self.errors = error.get('errors')
        except:  # Amazon S3 error
            self.msg = resp.content or '[No message]'

    def __repr__(self):
        return '<GitHubError [{0}]>'.format(self.msg or self.code)

    def __str__(self):
        return '{0} {1}'.format(self.code, self.msg)

    @property
    def message(self):
        return self.msg
