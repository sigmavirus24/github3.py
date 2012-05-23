"""
github3.models
==============

This module provides the basic models used in github3.py

"""

from datetime import datetime
from json import dumps
from .compat import loads


class GitHubCore(object):
    """A basic class for the other classes."""
    def __init__(self, session=None):
        self._session = session
        self._github_url = 'https://api.github.com'
        self._time_format = '%Y-%m-%dT%H:%M:%SZ'

    def __repr__(self):
        return '<github3-core at 0x%x>' % id(self)

    def _delete(self, url, **kwargs):
        return self._session.delete(url, **kwargs)

    def _get(self, url, **kwargs):
        return self._session.get(url, **kwargs)

    def _patch(self, url, data=None, **kwargs):
        return self._session.patch(url, data, **kwargs)

    def _post(self, url, data=None, **kwargs):
        return self._session.post(url, data, **kwargs)

    def _put(self, url, data=None, **kwargs):
        return self._session.put(url, data, **kwargs)

    def _strptime(self, time_str):
        return datetime.strptime(time_str, self._time_format)


class Plan(object):
    def __init__(self, data):
        super(Plan, self).__init__()
        self._collab = data.get('collaborators')
        self._name = data.get('name')
        self._private = data.get('private_repos')
        self._space = data.get('space')

    def collaborators(self):
        return self._collab

    def is_free(self):
        return self._name == 'free'

    def name(self):
        return self._name

    def private_repos(self):
        return self._private

    def space(self):
        return self._space


_large = Plan({'name': 'large', 'private_repos': 50,
    'collaborators': 25, 'space': 0})
_medium = Plan({'name': 'medium', 'private_repos': 20,
    'collaborators': 10, 'space': 0})
_small = Plan({'name': 'small', 'private_repos': 10,
    'collaborators': 5, 'space': 0})
_micro = Plan({'name': 'micro', 'private_repos': 5,
    'collaborators': 1, 'space': 0})
_free = Plan({'name': 'free', 'private_repos': 0,
    'collaborators': 0, 'space': 0})

plans = {'large': _large, 'medium': _medium, 'small': _small,
        'micro': _micro, 'free': _free}


class User(GitHubCore):
    def __init__(self, data, session):
        super(User, self).__init__(session)

        # Public information
        ## e.g. https://api.github.com/users/self._login
        self._api_url = data.get('url')

        self._avatar = data.get('avatar_url')
        self._bio = data.get('bio')
        self._blog = data.get('blog')
        self._company = data.get('company')
        self._email = data.get('email')

        ## The number of people following this user
        self._followers = data.get('followers')

        ## The number of people this user follows
        self._following = data.get('following')

        ## The number of people this user folows
        self._grav_id = data.get('gravatar_id')

        self._hire = data.get('hireable')
        self._id = data.get('id')
        self._location = data.get('location')
        self._login = data.get('login')

        ## e.g. first_name last_name
        self._name = data.get('name')

        ## The number of public_gists
        self._public_gists = data.get('public_gists')

        ## The number of public_repos
        self._public_repos = data.get('public_repos')

        ## e.g. https://github.com/self._login
        self._url = data.get('html_url')

        # Private information
        self._disk = data.get('disk_usage')
        if data.get('plan'):
            _plan = data.get('plan')
            self._plan = plans[_plan['name'].lower()]
            self._plan._space = _plan['space']
        else:
            self._plan = None

        ## The number of private repos
        self._private_repos = data.get('total_private_repos')
        self._private_gists = data.get('total_private_gists')

        self._owned_private_repos = data.get('owned_private_repos')

    def __repr__(self):
        return '<User [%s:%s]>' % (self._login, self._name)

    @property
    def avatar(self):
        return self._avatar

    @property
    def bio(self):
        return self._bio

    @property
    def blog(self):
        return self._blog

    @property
    def company(self):
        return self._company

    @property
    def disk_usage(self):
        return self._disk

    @property
    def email(self):
        return self._email

    @property
    def followers(self):
        return self._followers

    @property
    def following(self):
        return self._following

    @property
    def for_hire(self):
        return self._hire

    @property
    def html_url(self):
        return self._url

    @property
    def id(self):
        return self._id

    @property
    def location(self):
        return self._location

    @property
    def login(self):
        return self._login

    @property
    def name(self):
        return self._name

    @property
    def owned_private_repos(self):
        return self._owned_private_repos

    @property
    def private_gists(self):
        return self._private_gists

    @property
    def plan(self):
        return self._plan

    @property
    def public_gists(self):
        return self._public_gists

    @property
    def public_repos(self):
        return self._public_repos

    @property
    def total_private_repos(self):
        return self._private_repos


class BaseComment(GitHubCore):
    """A basic class for Gist, Issue and Pull Request Comments."""
    def __init__(self, comment, session):
        super(BaseComment, self).__init__(session)
        self._update_(comment)

    def __repr__(self):
        return '<github3-comment at 0x%x>' % id(self)

    def _update_(self, comment):
        self._id = comment.get('id')
        self._body = comment.get('body')
        self._user = User(comment.get('user'), self._session)
        self._created = self._strptime(comment.get('created_at'))
        self._updated = self._strptime(comment.get('updated_at'))

        self._api_url = comment.get('url')
        if comment.get('_links'):
            self._url = comment['_links'].get('html')
            self._pull = comment['_links'].get('pull_request')

        self._path = comment.get('path')
        self._pos = comment.get('position')
        self._cid = comment.get('comment_id')

    @property
    def body(self):
        return self._body

    @property
    def created_at(self):
        return self._created

    def delete(self):
        """Delete this comment."""
        resp = self._delete(self._api_url)
        if resp.status_code == 204:
            return True
        return False

    def edit(self, body):
        """Edit this comment."""
        if body:
            resp = self._patch(self._api_url, dumps({'body': body}))
            if resp.status_code == 200:
                self._update_(loads(resp.content))
                return True
        return False

    @property
    def id(self):
        return self._id

    @property
    def user(self):
        return self._user
