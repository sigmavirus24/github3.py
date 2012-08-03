"""
github3.models
==============

This module provides the basic models used in github3.py

"""

from datetime import datetime
from json import dumps
from requests import session
from re import compile
from functools import wraps

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
        if ses is None:
            ses = session()
        self._session = ses
        self._github_url = 'https://api.github.com'
        self._time_format = '%Y-%m-%dT%H:%M:%SZ'
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
            kwargs.update(headers={'Content-Length': '0'})
            req = self._session.put(url, **kwargs)
        return req

    def _strptime(self, time_str):
        """Converts an ISO 8601 formatted string into a datetime object."""
        if time_str:
            return datetime.strptime(time_str, self._time_format)
        else:
            return None

    def _build_url(self, *args, **kwargs):
        """Builds a new API url from scratch."""
        parts = [kwargs.get('base_url') or self._github_url]
        parts.extend(args)
        key = tuple(parts)
        if not key in __url_cache__:
            __url_cache__[key] = '/'.join(parts)
        return __url_cache__[key]

    @property
    def ratelimit_remaining(self):
        """Number of requests before GitHub imposes a ratelimit."""
        json = self._get(self._github_url + '/rate_limit')
        self._remaining = json.get('rate', {}).get('remaining', 0)
        return self._remaining

    @staticmethod
    def requires_auth(func):
        """Decorator to note which object methods require authorization."""
        note = """
        .. note::
            The signature of this function may not appear correctly in
            documentation. Please adhere to the defined parameters and their
            types.
        """
        func.__doc__ = '\n'.join([func.__doc__, note])

        @wraps(func)
        def auth_wrapper(self, *args, **kwargs):
            auth = False
            if hasattr(self, '_session'):
                auth = self._session.auth or \
                    self._session.headers.get('Authorization')

            if auth:
                return func(self, *args, **kwargs)
            else:
                raise GitHubError(type('Faux Request', (object, ),
                    {'status_code': 401, 'json': {
                        'message': 'Requires authentication'}}
                    ))
        return auth_wrapper


class BaseComment(GitHubCore):
    """The :class:`BaseComment <BaseComment>` object. A basic class for Gist,
    Issue and Pull Request Comments."""
    def __init__(self, comment, session):
        super(BaseComment, self).__init__(comment, session)
        self._update_(comment)

    def __repr__(self):
        return '<github3-comment at 0x{0:x}>'.format(id(self))

    def _update_(self, comment):
        self._json_data = comment
        self._id = comment.get('id')
        self._body = comment.get('body')
        self._bodyt = comment.get('body_text')
        self._bodyh = comment.get('body_html')
        self._created = self._strptime(comment.get('created_at'))
        self._updated = self._strptime(comment.get('updated_at'))

        self._api = comment.get('url')
        if comment.get('_links'):
            self._url = comment['_links'].get('html')
            self._pull = comment['_links'].get('pull_request')

        self._path = comment.get('path')
        self._pos = comment.get('position')
        self._cid = comment.get('commit_id')

    @property
    def body(self):
        """Body of the comment. (As written by the commenter)"""
        return self._body

    @property
    def body_html(self):
        """Body of the comment formatted as html."""
        return self._bodyh

    @property
    def body_text(self):
        """Body of the comment formatted as plain-text. (Stripped of markdown,
        etc.)"""
        return self._bodyt

    @property
    def created_at(self):
        """datetime object representing when the comment was created."""
        return self._created

    @GitHubCore.requires_auth
    def delete(self):
        """Delete this comment.

        :returns: bool
        """
        return self._boolean(self._delete(self._api), 204, 404)

    @GitHubCore.requires_auth
    def edit(self, body):
        """Edit this comment.

        :param body: (required), new body of the comment, Markdown formatted
        :type body: str
        :returns: bool
        """
        if body:
            json = self._patch(self._api, dumps({'body': body}))
            if json:
                self._update_(json)
                return True
        return False

    @property
    def id(self):
        """Unique ID of the comment."""
        return self._id

    @property
    def user(self):
        """:class:`User <github3.user.User>` who created the comment."""
        return self._user


class BaseCommit(GitHubCore):
    """The :class:`BaseCommit <BaseCommit>` object. This serves as the base for
    the various types of commit objects returned by the API.
    """
    def __init__(self, commit, session):
        super(BaseCommit, self).__init__(commit, session)
        self._api = commit.get('url')
        self._sha = commit.get('sha')
        self._msg = commit.get('message')
        self._parents = commit.get('parents', [])
        if not self._sha:
            i = self._api.rfind('/')
            self._sha = self._api[i + 1:]

    @property
    def message(self):
        """Commit message"""
        return self._msg

    @property
    def parents(self):
        """List of parents to this commit."""
        return self._parents

    @property
    def sha(self):
        """SHA of this commit."""
        return self._sha


class BaseAccount(GitHubCore):
    """The :class:`BaseAccount <BaseAccount>` object. This is used to do the
    heavy lifting for :class:`Organization <github3.org.Organization>` and
    :class:`User <github3.user.User>` objects.
    """
    def __init__(self, acct, session):
        super(BaseAccount, self).__init__(acct, session)
        self._update_(acct)

    def __repr__(self):
        return '<BaseAccount [%s:%s]>' % (self._login, self._name)

    def _update_(self, acct):
        # Public information
        ## e.g. https://api.github.com/users/self._login
        self._json_data = acct
        self._type = None
        if acct.get('type'):
            self._type = acct.get('type')
        self._api = acct.get('url', '')

        self._avatar = acct.get('avatar_url', '')
        self._blog = acct.get('blog', '')
        self._company = acct.get('company', '')

        self._created = None
        if acct.get('created_at'):
            self._created = self._strptime(acct.get('created_at'))
        self._email = acct.get('email')

        ## The number of people following this acct
        self._followers = acct.get('followers', 0)

        ## The number of people this acct follows
        self._following = acct.get('following', 0)

        self._id = acct.get('id', 0)
        self._location = acct.get('location', '')
        self._login = acct.get('login', '')

        ## e.g. first_name last_name
        self._name = acct.get('name', '')

        ## The number of public_repos
        self._public_repos = acct.get('public_repos', 0)

        ## e.g. https://github.com/self._login
        self._url = acct.get('html_url', '')

        ## The number of private repos
        if self._type == 'Organization':
            self._private_repos = acct.get('private_repos', 0)

        self._bio = acct.get('bio')
        if self._type == 'User':

            ## The number of people this acct folows
            self._grav_id = acct.get('gravatar_id', '')
            self._hire = acct.get('hireable', False)

            ## The number of public_gists
            self._public_gists = acct.get('public_gists', 0)

            # Private information
            self._disk = acct.get('disk_usage', 0)

            self._owned_private_repos = acct.get('owned_private_repos', 0)
            self._private_gists = acct.get('total_private_gists', 0)
            self._private_repos = acct.get('total_private_repos', 0)

    @property
    def avatar_url(self):
        """URL of the avatar at gravatar"""
        return self._avatar

    @property
    def bio(self):
        """Markdown formatted biography"""
        return self._bio

    @property
    def blog(self):
        """URL of the blog"""
        return self._blog

    @property
    def company(self):
        """Name of the company"""
        return self._company

    @property
    def created_at(self):
        """datetime object representing the date the account was created"""
        return self._created

    @property
    def email(self):
        """E-mail address of the user/org"""
        return self._email

    @property
    def followers(self):
        """Number of followers"""
        return self._followers

    @property
    def following(self):
        """Number of people the user is following"""
        return self._following

    @property
    def html_url(self):
        """URL of the user/org's profile"""
        return self._url

    @property
    def id(self):
        """Unique ID of the user/org"""
        return self._id

    @property
    def location(self):
        """Location of the user/org"""
        return self._location

    @property
    def login(self):
        """login name of the user/org"""
        return self._login

    @property
    def name(self):
        """Real name of the user/org"""
        return self._name

    @property
    def public_repos(self):
        """Number of public repos owned by the user/org"""
        return self._public_repos


class GitHubError(Exception):
    def __init__(self, resp):
        super(GitHubError, self).__init__()
        self._code = resp.status_code
        error = resp.json
        self._message = error.get('message')
        self._errors = []
        if error.get('errors'):
            self._errors = error.get('errors')

    def __repr__(self):
        return '<Error [{0}]>'.format(self._message or self._code)

    def __str__(self):
        if not self._errors:
            return '{0} {1}'.format(self._code, self._message)
        else:
            return '{0} {1}: {2}'.format(self._code, self._message,
                ', '.join(self._errors))

    @property
    def code(self):
        return self._code

    @property
    def errors(self):
        return self._errors

    @property
    def message(self):
        return self._message
