"""
github3.models
==============

This module provides the basic models used in github3.py

"""

from datetime import datetime
from json import dumps
from requests import session
from re import compile
from github3.decorators import requires_auth

try:  # (No coverage)
    # Python 2.x
    from urlparse import urlparse  # (No coverage)
except ImportError:  # (No coverage)
    # Python 3.x
    from urllib.parse import urlparse  # (No coverage)

__url_cache__ = {}


class GitHubObject(object):
    """The :class:`GitHubObject <GitHubObject>` object. A basic class to be
    subclassed by GitHubCore and other classes that would otherwise subclass
    object."""
    def __init__(self, json):
        super(GitHubObject, self).__init__()
        self._json_data = json

    def to_json(self):
        """Return the json representing this object."""
        return self._json_data

    def _strptime(self, time_str):
        """Converts an ISO 8601 formatted string into a datetime object."""
        if time_str:
            return datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')
        else:
            return None

    @classmethod
    def from_json(cls, json):
        """Return an instance of ``cls`` formed from ``json``."""
        return cls(json)


class GitHubCore(GitHubObject):
    """The :class:`GitHubCore <GitHubCore>` object. This class provides some
    basic attributes to other classes that are very useful to have.
    """
    def __init__(self, json, ses=None):
        super(GitHubCore, self).__init__(json)
        if hasattr(ses, '_session'):
            # i.e. session is actually a GitHub object
            ses = ses._session
        elif ses is None:
            ses = session()
        self._session = ses

        # Only accept JSON responses
        self._session.headers.update(
                {'Accept': 'application/vnd.github.v3.full+json'})
        # Only accept UTF-8 encoded data
        self._session.headers.update({'Accept-Charset': 'utf-8'})
        # Identify who we are
        self._session.config['base_headers'].update(
                {'User-Agent': 'github3.py/pre-alpha'})

        # set a sane default
        self._github_url = 'https://api.github.com'
        self._remaining = 5000
        self._rel_reg = compile(r'<(https://[0-9a-zA-Z\./\?=&]+)>; '
                'rel="(\w+)"')

    def __repr__(self):
        return '<github3-core at 0x{0:x}>'.format(id(self))

    def _json(self, request, status_code):
        ret = None
        if request.status_code == status_code and request.content:
            ret = request.json
        if request.status_code >= 400:
            raise GitHubError(request)
        return ret

    def _boolean(self, request, true_code, false_code):
        if request.status_code == true_code:
            return True
        if request.status_code != false_code and request.status_code >= 400:
            raise GitHubError(request)
        return False

    def _delete(self, url, **kwargs):
        req = False
        if self._remaining > 0:
            req = self._session.delete(url, **kwargs)
        return req

    def _get(self, url, **kwargs):
        req = None
        if self._remaining > 0:
            req = self._session.get(url, **kwargs)
        return req

    def _patch(self, url, **kwargs):
        req = None
        if self._remaining > 0:
            req = self._session.patch(url, **kwargs)
        return req

    def _post(self, url, data=None, **kwargs):
        req = None
        if self._remaining > 0:
            req = self._session.post(url, data, **kwargs)
        return req

    def _put(self, url, **kwargs):
        req = False
        if self._remaining > 0:
            if 'data' not in kwargs:
                kwargs.update(headers={'Content-Length': '0'})
            req = self._session.put(url, **kwargs)
        return req

    def _build_url(self, *args, **kwargs):
        """Builds a new API url from scratch."""
        parts = [kwargs.get('base_url') or self._github_url]
        parts.extend(args)
        key = tuple(parts)
        if not key in __url_cache__:
            __url_cache__[key] = '/'.join(parts)
        return __url_cache__[key]

    @property
    def _api(self):
        return "{0.scheme}://{0.netloc}{0.path}".format(self._uri)

    @_api.setter
    def _api(self, uri):
        self._uri = urlparse(uri)

    def _iter(self, count, url, cls, core_obj=True):
        """Generic iterator for this project.

        :param int count: How many items to return.
        :param int url: First URL to start with
        :param class cls: cls to return an object of
        :param bool core_obj: whether this class derives from GitHubCore
            object or not. If not it derives from GitHubObject and has no
            second parameter.
        """
        while (count == -1 or count > 0) and url:
            response = self._get(url)
            json = self._json(response, 200)
            for i in json:
                yield cls(i, self) if core_obj else cls(i)
                count -= 1 if count > 0 else 0
                if count == 0:
                    break

            rel_next = response.links.get('next', {})
            url = rel_next.get('url', '')

    @property
    def ratelimit_remaining(self):
        """Number of requests before GitHub imposes a ratelimit."""
        json = self._json(self._get(self._github_url + '/rate_limit'), 200)
        self._remaining = json.get('rate', {}).get('remaining', 0)
        return self._remaining

    @classmethod
    def from_json(cls, json):
        """Return an instance of ``cls`` formed from ``json``."""
        return cls(json, None)


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
        if not self.sha:
            i = self._api.rfind('/')
            self.sha = self._api[i + 1:]


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
        self.name = acct.get('name', '')

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
        error = resp.json
        #: Message associated with the error
        self.msg = error.get('message')
        #: List of errors provided by GitHub
        self.errors = []
        if error.get('errors'):
            self.errors = error.get('errors')

    def __repr__(self):
        return '<GitHubError [{0}]>'.format(self.msg or self.code)

    def __str__(self):
        return '{0} {1}'.format(self.code, self.msg)

    @property
    def message(self):
        return self.msg
