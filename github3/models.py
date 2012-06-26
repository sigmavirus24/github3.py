"""
github3.models
==============

This module provides the basic models used in github3.py

"""

from datetime import datetime
from json import dumps


class GitHubCore(object):
    """The :class:`GitHubCore <GitHubCore>` object. This class provides some
    basic attributes to other classes that are very useful to have.
    """
    def __init__(self, session=None):
        self._session = session
        if self._session:
            setattr(self._session, '_remain', 5000)
        self._github_url = 'https://api.github.com'
        self._time_format = '%Y-%m-%dT%H:%M:%SZ'
        self._remaining = 5000

    def __repr__(self):
        return '<github3-core at 0x%x>' % id(self)

    def _json(self, request, status_code):
        if request.status_code == status_code:
            return request.json if request.content else True
        if request.status_code >= 400:
            raise Error(request)
        return None

    def _getr(self, url, status_code=200, **kwargs):
        # In the rare instance we care about the entire response.
        req = None
        if self._remaining > 0:
            req = self._session.get(url, **kwargs)
            if req.status_code != status_code or req.status_code >= 400:
                raise Error(request)
        return req

    def _boolean(self, request, status_code):
        if request.status_code == status_code:
            return True
        if request.status_code != 404 and request.status_code >= 400:
            raise Error(request)
        return False

    def _delete(self, url, status_code=204, **kwargs):
        req = False
        if self._remaining > 0:
            req = self._session.delete(url, **kwargs)
            req = self._boolean(req, status_code)
        return req

    def _get(self, url, status_code=200, **kwargs):
        req = None
        if self._remaining > 0:
            req = self._session.get(url, **kwargs)
            if status_code == 204:
                # We're not expecting any json back
                # If we left it as a simple _json() call there would be a
                #  TypeError since requests doesn't handle that cleanly
                req = self._boolean(req, status_code)
            else:
                req = self._json(req, status_code)
        return req

    def _patch(self, url, data=None, status_code=200, **kwargs):
        req = None
        if self._remaining > 0:
            req = self._session.patch(url, data, **kwargs)
            req = self._json(req, status_code)
        return req

    def _post(self, url, data=None, status_code=201, **kwargs):
        req = None
        if self._remaining > 0:
            req = self._session.post(url, data, **kwargs)
            req = self._json(req, status_code)
        return req

    def _put(self, url, data=None, status_code=204, **kwargs):
        req = False
        if self._remaining > 0:
            kwargs.update(headers={'Content-Length': '0'})
            req = self._session.put(url, data, **kwargs)
            req = self._boolean(req, status_code)
        return req

    def _strptime(self, time_str):
        """Converts an ISO 8601 formatted string into a datetime object."""
        if time_str:
            return datetime.strptime(time_str, self._time_format)
        else:
            return None

    @property
    def ratelimit_remaining(self):
        """Number of requests before GitHub imposes a ratelimit."""
        json = self._get(self._github_url + '/rate_limit')
        return json.get('rate', {}).get('remaining', 5000)


class BaseComment(GitHubCore):
    """The :class:`BaseComment <BaseComment>` object. A basic class for Gist,
    Issue and Pull Request Comments."""
    def __init__(self, comment, session):
        super(BaseComment, self).__init__(session)
        self._update_(comment)

    def __repr__(self):
        return '<github3-comment at 0x%x>' % id(self)

    def _update_(self, comment):
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

    def delete(self):
        """Delete this comment.
        
        :returns: bool
        """
        return self._delete(self._api)

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
        """:class:`User <user.User>` who created the comment."""
        return self._user


class BaseCommit(GitHubCore):
    """The :class:`BaseCommit <BaseCommit>` object. This serves as the base for
    the various types of commit objects returned by the API.
    """
    def __init__(self, commit, session):
        super(BaseCommit, self).__init__(session)
        self._api = commit.get('url')
        self._sha = commit.get('sha')
        self._msg = commit.get('message')
        self._parents = commit.get('parents', [])

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
    heavy lifting for :class:`Organization <org.Organization>` and :class:`User
    <user.User>` objects.
    """
    def __init__(self, acct, session):
        super(BaseAccount, self).__init__(session)
        self._update_(acct)

    def __repr__(self):
        return '<BaseAccount [%s:%s]>' % (self._login, self._name)

    def _update_(self, acct):
        # Public information
        ## e.g. https://api.github.com/users/self._login
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

class Error(BaseException):
    def __init__(self, resp):
        super(Error, self).__init__()
        self._code = resp.status_code
        error = resp.json
        self._message = error.get('message')
        self._errors = []
        if error.get('errors'):
            self._errors = error.get('errors')

    def __repr__(self):
        return '<Error [%s]>' % (self._message or self._code)

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
