"""
github3.models
==============

This module provides the basic models used in github3.py

"""

from json import dumps
from requests import session
from requests.compat import urlparse
from github3.decorators import requires_auth
from github3.packages.PySO8601 import parse
from github3 import __version__

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
        return parse(time_str) if time_str else None

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
        headers = {
            # Only accept JSON responses
            'Accept': 'application/vnd.github.v3.full+json',
            # Only accept UTF-8 encoded data
            'Accept-Charset': 'utf-8',
            # Always sending JSON
            'Content-Type': "application/json",
            # Set our own custom User-Agent string
            'User-Agent': 'github3.py/{0}'.format(__version__),
        }

        self._session.headers.update(headers)

        # set a sane default
        self._github_url = 'https://api.github.com'

    def __repr__(self):
        return '<github3-core at 0x{0:x}>'.format(id(self))

    def _remove_none(self, data):
        for (k, v) in list(data.items()):
            if v is None:
                del(data[k])

    def _json(self, response, status_code):
        ret = None
        if response.status_code == status_code and response.content:
            ret = response.json()
        if response.status_code >= 400:
            raise GitHubError(response)
        return ret

    def _boolean(self, request, true_code, false_code):
        if request.status_code == true_code:
            return True
        if request.status_code != false_code and request.status_code >= 400:
            raise GitHubError(request)
        return False

    def _delete(self, url, **kwargs):
        return self._session.delete(url, **kwargs)

    def _get(self, url, **kwargs):
        return self._session.get(url, **kwargs)

    def _patch(self, url, **kwargs):
        return self._session.patch(url, **kwargs)

    def _post(self, url, data=None, **kwargs):
        return self._session.post(url, data, **kwargs)

    def _put(self, url, **kwargs):
        return self._session.put(url, **kwargs)

    def _build_url(self, *args, **kwargs):
        """Builds a new API url from scratch."""
        parts = [kwargs.get('base_url') or self._github_url]
        parts.extend(args)
        parts = [str(p) for p in parts]
        key = tuple(parts)
        if not key in __url_cache__:
            __url_cache__[key] = '/'.join(parts)
        return __url_cache__[key]

    @property
    def api(self):
        return "{0.scheme}://{0.netloc}{0.path}".format(self._uri)

    @api.setter
    def api(self, uri):
        self._uri = urlparse(uri)

    def _iter(self, count, url, cls, params=None):
        """Generic iterator for this project.

        :param int count: How many items to return.
        :param int url: First URL to start with
        :param class cls: cls to return an object of
        :param params dict: (optional) Parameters for the request
        """
        while (count == -1 or count > 0) and url:
            response = self._get(url, params=params)
            if params:
                params = None  # rel_next contains the params
            json = self._json(response, 200)

            # languages returns a single dict. We want the items.
            if isinstance(json, dict):
                json = json.items()

            for i in json:
                yield cls(i, self) if issubclass(cls, GitHubCore) else cls(i)
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

    def refresh(self):
        """Re-retrieve the information for this object and returns the
        refreshed instance."""
        json = self._json(self._get(self._api), 200)
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
        self.name = acct.get('name', '').encode('utf-8')

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
        if resp.json():  # GitHub Error
            error = resp.json()
            #: Message associated with the error
            self.msg = error.get('message')
            #: List of errors provided by GitHub
            if error.get('errors'):
                self.errors = error.get('errors')
        else:  # Amazon S3 error
            self.msg = resp.content or '[No message]'

    def __repr__(self):
        return '<GitHubError [{0}]>'.format(self.msg or self.code)

    def __str__(self):
        return '{0} {1}'.format(self.code, self.msg)

    @property
    def message(self):
        return self.msg
