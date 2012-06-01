"""
github3.user
============

This module contains everything relating to Users.

"""

from json import dumps
from .models import GitHubCore, BaseAccount


class Key(GitHubCore):
    def __init__(self, key, session):
        super(Key, self).__init__(session)
        self._update_(key)

    def __repr__(self):
        return '<User Key [%s]>' % self._title

    def _update_(self, key):
        self._api = key.get('url')
        self._id = key.get('id')
        self._title = key.get('title')
        self._key = key.get('key')

    def delete(self):
        return self._delete(self._api)

    @property
    def key(self):
        return self._key

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    def update(self, title, key):
        if not title:
            title = self._title
        if not key:
            key = self._key

        json = self._patch(self._api, dumps({'title': title,
            'key': key}))
        if json:
            self._update_(json)
            return True
        return False


class Plan(object):
    def __init__(self, plan):
        super(Plan, self).__init__()
        self._collab = plan.get('collaborators')
        self._name = plan.get('name')
        self._private = plan.get('private_repos')
        self._space = plan.get('space')

    def __repr__(self):
        return '<Plan [%s]>' % self._name

    @property
    def collaborators(self):
        return self._collab

    @property
    def is_free(self):
        return self._name == 'free'

    @property
    def name(self):
        return self._name

    @property
    def private_repos(self):
        return self._private

    @property
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


class User(BaseAccount):
    def __init__(self, user, session):
        super(User, self).__init__(user, session)
        self._update_(user)
        if not self._type:
            self._type = 'User'

    def __repr__(self):
        return '<User [%s:%s]>' % (self._login, self._name)

    def _update_(self, user):
        # Private information
        super(User, self)._update_(user)
        if user.get('plan'):
            _plan = user.get('plan')
            self._plan = plans[_plan['name'].lower()]
            self._plan._space = _plan['space']
        else:
            self._plan = None

    def add_email_addresses(self, addresses=[]):
        """Add the email addresses in ``addresses`` to the authenticated
        user's account."""
        json = []
        if addresses:
            url = self._github_url + '/user/emails'
            json = self._post(url, dumps(addresses))
        return json

    def delete_email_addresses(self, addresses=[]):
        """Delete the email addresses in ``addresses`` from the
        authenticated user's account."""
        url = self._github_url + '/user/emails'
        return self._delete(url, data=dumps(addresses))

    @property
    def disk_usage(self):
        return self._disk

    @property
    def for_hire(self):
        return self._hire

    def list_emails(self):
        """List email addresses for a user.

        Predicated on the assumption that you're authenticated for this
        user.
        """
        url = self._github_url + '/user/emails'
        return self._get(url) or []

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
    def total_private_repos(self):
        return self._private_repos

    def update(self, name=None, email=None, blog=None, company=None,
            location=None, hireable=False, bio=None):
        """If authenticated as this user, update the information with
        the information provided in the parameters.

        :param name: string, e.g., 'John Smith', not login name
        :param email: string, e.g., 'john.smith@example.com'
        :param blog: string, e.g., 'http://www.example.com/jsmith/blog'
        :param company: string
        :param location: string
        :param hireable: boolean, defaults to False
        :param bio: string, GitHub flavored markdown
        """
        user = dumps({'name': name, 'email': email, 'blog': blog,
            'company': company, 'location': location,
            'hireable': hireable, 'bio': bio})
        url = self._github_url + '/user'
        json = self._patch(url, user)
        if json:
            self._update_(json)
            return True
        return False
