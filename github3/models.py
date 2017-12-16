# -*- coding: utf-8 -*-
"""
github3.models
==============

This module provides the basic models used in github3.py

"""
from __future__ import unicode_literals

import dateutil.parser
from json import dumps, loads
from logging import getLogger

import requests
from requests.compat import is_py2, urlparse

from . import exceptions
from .decorators import requires_auth
from .session import GitHubSession

__timeformat__ = '%Y-%m-%dT%H:%M:%SZ'
__logs__ = getLogger(__package__)


class GitHubCore(object):
    """The base object for all objects that require a session.

    The :class:`GitHubCore <GitHubCore>` object provides some
    basic attributes and methods to other sub-classes that are very useful to
    have.
    """

    def __init__(self, json, session=None):
        if hasattr(session, 'session'):
            # i.e. session is actually a GitHubCore instance
            session = session.session
        elif session is None:
            session = GitHubSession()
        self.session = session

        # set a sane default
        self._github_url = 'https://api.github.com'

        if json is not None:
            self.etag = json.pop('ETag', None)
            self.last_modified = json.pop('Last-Modified', None)
            self._uniq = json.get('url', None)
        self._json_data = json
        try:
            self._update_attributes(json)
        except KeyError as kerr:
            raise exceptions.IncompleteResponse(json, kerr)

    def _update_attributes(self, json):
        pass

    def __getattr__(self, attribute):
        """Proxy access to stored JSON."""
        if attribute not in self._json_data:
            raise AttributeError(attribute)
        value = self._json_data.get(attribute)
        setattr(self, attribute, value)
        return value

    def as_dict(self):
        """Return the attributes for this object as a dictionary.

        This is equivalent to calling::

            json.loads(obj.as_json())

        :returns: this object's attributes serialized to a dictionary
        :rtype: dict
        """
        return self._json_data

    def as_json(self):
        """Return the json data for this object.

        This is equivalent to calling::

            json.dumps(obj.as_dict())

        :returns: this object's attributes as a JSON string
        :rtype: str
        """
        return dumps(self._json_data)

    @classmethod
    def _get_attribute(cls, data, attribute, fallback=None):
        """Return the attribute from the json data.

        :param dict data: dictionary used to put together the model
        :param str attribute: key of the attribute
        :param any fallback: return value if original return value is falsy
        :returns: value paired with key in dict, fallback
        """
        if data is None or not isinstance(data, dict):
            return None
        result = data.get(attribute)
        if result is None:
            return fallback
        return result

    @classmethod
    def _class_attribute(cls, data, attribute, cl, *args, **kwargs):
        """Return the attribute from the json data and instantiate the class.

        :param dict data: dictionary used to put together the model or None
        :param str attribute: key of the attribute
        :param class cl: class that will be instantiated
        :returns: instantiated class or None
        :rtype: object or None
        """
        value = cls._get_attribute(data, attribute)
        if value:
            return cl(
                value,
                *args,
                **kwargs
            )
        return value

    @classmethod
    def _strptime_attribute(cls, data, attribute):
        """Get a datetime object from a dict, return None if it wan't found.

        This is equivalent to calling::

            cls._strptime(data[attribute]) if attribute in data else None

        :param dict data: dictionary used to put together the model
        :param str attribute: key of the attribute
        :returns: timezone-aware datetime object
        :rtype: datetime
        """
        result = cls._get_attribute(data, attribute)
        if result:
            return cls._strptime(result)
        return result

    @classmethod
    def _strptime(cls, time_str):
        """Convert an ISO 8601 formatted string to a datetime object.

        We assume that the ISO 8601 formatted string is in UTC and we create
        the datetime object so that it is timezone-aware.

        :param str time_str: ISO 8601 formatted string
        :returns: timezone-aware datetime object
        :rtype: datetime or None
        """
        if time_str:
            # Parse ISO8601 string using python-dateutil
            return dateutil.parser.parse(time_str)
        return None

    def __repr__(self):
        repr_string = self._repr()
        if is_py2:
            return repr_string.encode('utf-8')
        return repr_string

    @classmethod
    def from_dict(cls, json_dict):
        """Return an instance of this class formed from ``json_dict``."""
        return cls(json_dict)

    @classmethod
    def from_json(cls, json):
        """Return an instance of this class formed from ``json``."""
        return cls(loads(json))

    def __eq__(self, other):
        return self._uniq == other._uniq

    def __ne__(self, other):
        return self._uniq != other._uniq

    def __hash__(self):
        return hash(self._uniq)

    def _repr(self):
        return '<github3-core at 0x{0:x}>'.format(id(self))

    @staticmethod
    def _remove_none(data):
        if not data:
            return
        for (k, v) in list(data.items()):
            if v is None:
                del(data[k])

    def _instance_or_null(self, instance_class, json):
        if json is not None and not isinstance(json, dict):
            raise exceptions.UnprocessableResponseBody(
                "GitHub's API returned a body that could not be handled", json
            )
        if not json:
            return None
        try:
            return instance_class(json, self)
        except TypeError:  # instance_class is not a subclass of GitHubCore
            return instance_class(json)

    def _json(self, response, status_code, include_cache_info=True):
        ret = None
        if self._boolean(response, status_code, 404) and response.content:
            __logs__.info('Attempting to get JSON information from a Response '
                          'with status code %d expecting %d',
                          response.status_code, status_code)
            ret = response.json()
            headers = response.headers
            if (include_cache_info and
                    (headers.get('Last-Modified') or headers.get('ETag')) and
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
                raise exceptions.error_for(response)
        return False

    def _request(self, method, *args, **kwargs):
        try:
            request_method = getattr(self.session, method)
            return request_method(*args, **kwargs)
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                ) as exc:
            raise exceptions.ConnectionError(exc)
        except requests.exceptions.RequestException as exc:
            raise exceptions.TransportError(exc)

    def _delete(self, url, **kwargs):
        __logs__.debug('DELETE %s with %s', url, kwargs)
        return self._request('delete', url, **kwargs)

    def _get(self, url, **kwargs):
        __logs__.debug('GET %s with %s', url, kwargs)
        return self._request('get', url, **kwargs)

    def _patch(self, url, **kwargs):
        __logs__.debug('PATCH %s with %s', url, kwargs)
        return self._request('patch', url, **kwargs)

    def _post(self, url, data=None, json=True, **kwargs):
        if json:
            data = dumps(data) if data is not None else data
        __logs__.debug('POST %s with %s, %s', url, data, kwargs)
        return self._request('post', url, data, **kwargs)

    def _put(self, url, **kwargs):
        __logs__.debug('PUT %s with %s', url, kwargs)
        return self._request('put', url, **kwargs)

    def _build_url(self, *args, **kwargs):
        """Builds a new API url from scratch."""
        return self.session.build_url(*args, **kwargs)

    @property
    def _api(self):
        value = "{0.scheme}://{0.netloc}{0.path}".format(self._uri)
        if self._uri.query:
            value += '?{}'.format(self._uri.query)
        return value

    @_api.setter
    def _api(self, uri):
        if uri:
            self._uri = urlparse(uri)
        self.url = uri

    def _iter(self, count, url, cls, params=None, etag=None, headers=None):
        """Generic iterator for this project.

        :param int count: How many items to return.
        :param int url: First URL to start with
        :param class cls: cls to return an object of
        :param params dict: (optional) Parameters for the request
        :param str etag: (optional), ETag from the last call
        :param dict headers: (optional) HTTP Headers for the request
        :returns: A lazy iterator over the pagianted resource
        :rtype: :class:`GitHubIterator <github3.structs.GitHubIterator>`
        """
        from .structs import GitHubIterator
        return GitHubIterator(count, url, cls, self, params, etag, headers)

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
        """Re-retrieve the information for this object.

        The reasoning for the return value is the following example: ::

            repos = [r.refresh() for r in g.repositories_by('kennethreitz')]

        Without the return value, that would be an array of ``None``'s and you
        would otherwise have to do: ::

            repos = [r for i in g.repositories_by('kennethreitz')]
            [r.refresh() for r in repos]

        Which is really an anti-pattern.

        .. versionchanged:: 0.5

        .. _Conditional Requests:
            http://developer.github.com/v3/#conditional-requests

        :param bool conditional: If True, then we will search for a stored
            header ('Last-Modified', or 'ETag') on the object and send that
            as described in the `Conditional Requests`_ section of the docs
        :returns: self
        """
        headers = getattr(self, 'CUSTOM_HEADERS', {})
        if conditional:
            if self.last_modified:
                headers['If-Modified-Since'] = self.last_modified
            elif self.etag:
                headers['If-None-Match'] = self.etag

        headers = headers or None
        json = self._json(self._get(self._api, headers=headers), 200)
        if json is not None:
            self._json_data = json
            self._update_attributes(json)
        return self


class BaseComment(GitHubCore):

    """A basic class for Gist, Issue and Pull Request Comments."""

    def _update_attributes(self, comment):
        #: Unique ID of the comment.
        self.id = self._get_attribute(comment, 'id')

        #: Body of the comment. (As written by the commenter)
        self.body = self._get_attribute(comment, 'body')

        #: Body of the comment formatted as plain-text. (Stripped of markdown,
        #: etc.)
        self.body_text = self._get_attribute(comment, 'body_text')

        #: Body of the comment formatted as html.
        self.body_html = self._get_attribute(comment, 'body_html')

        #: datetime object representing when the comment was created.
        self.created_at = self._strptime_attribute(comment, 'created_at')

        #: datetime object representing when the comment was updated.
        self.updated_at = self._strptime_attribute(comment, 'updated_at')

        self._api = self._get_attribute(comment, 'url')
        self.links = self._get_attribute(comment, '_links', {})
        #: The url of this comment at GitHub
        self.html_url = ''

        #: The url of the pull request, if it exists
        self.pull_request_url = ''
        if self.links:
            self.html_url = self.links.get('html')
            self.pull_request_url = self.links.get('pull_request')

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
                self._update_attributes(json)
                return True
        return False


class BaseCommit(GitHubCore):

    """This abstracts a lot of the common attributes for commit-like objects.

    The :class:`BaseCommit <BaseCommit>` object serves as the base for
    the various types of commit objects returned by the API.
    """

    def _update_attributes(self, commit):
        self._api = self._get_attribute(commit, 'url')

        #: SHA of this commit.
        self.sha = self._get_attribute(commit, 'sha')

        #: Commit message
        self.message = self._get_attribute(commit, 'message')

        #: List of parents to this commit.
        self.parents = self._get_attribute(commit, 'parents', [])

        #: URL to view the commit on GitHub
        self.html_url = self._get_attribute(commit, 'html_url')
        if not self.sha:
            i = self._api.rfind('/')
            self.sha = self._api[i + 1:]

        self._uniq = self.sha


class BaseAccount(GitHubCore):

    """This class holds the commonalities of Organizations and Users.

    The :class:`BaseAccount <BaseAccount>` object is used to do the
    heavy lifting for :class:`Organization <github3.orgs.Organization>` and
    :class:`User <github3.users.User>` objects.
    """

    def _update_attributes(self, acct):
        #: Tells you what type of account this is
        self.type = self._get_attribute(acct, 'type')

        self._api = self._get_attribute(acct, 'url')

        #: URL of the avatar at gravatar
        self.avatar_url = self._get_attribute(acct, 'avatar_url')

        #: URL of the blog
        self.blog = self._get_attribute(acct, 'blog')

        #: Name of the company
        self.company = self._get_attribute(acct, 'company')

        #: datetime object representing the date the account was created
        self.created_at = self._strptime_attribute(acct, 'created_at')

        #: E-mail address of the user/org
        self.email = self._get_attribute(acct, 'email')

        # The number of people following this acct
        #: Number of followers
        self.followers_count = self._get_attribute(acct, 'followers')

        # The number of people this acct follows
        #: Number of people the user is following
        self.following_count = self._get_attribute(acct, 'following')

        #: Unique ID of the account
        self.id = self._get_attribute(acct, 'id')

        #: Location of the user/org
        self.location = self._get_attribute(acct, 'location')

        #: User name of the user/organization
        self.login = self._get_attribute(acct, 'login')

        # e.g. first_name last_name
        #: Real name of the user/org
        self.name = self._get_attribute(acct, 'name')

        # The number of public_repos
        #: Number of public repos owned by the user/org
        self.public_repos_count = self._get_attribute(acct, 'public_repos')

        # e.g. https://github.com/self._login
        #: URL of the user/org's profile
        self.html_url = self._get_attribute(acct, 'html_url')

        #: Markdown formatted biography
        self.bio = self._get_attribute(acct, 'bio')

    def _repr(self):
        return '<{s.type} [{s.login}:{s.name}]>'.format(s=self)
