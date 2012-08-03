"""
github3.user
============

This module contains everything relating to Users.

"""

from json import dumps
from .events import Event
from .models import GitHubObject, GitHubCore, BaseAccount


class Key(GitHubCore):
    """The :class:`Key <Key>` object."""
    def __init__(self, key, session=None):
        super(Key, self).__init__(key, session)
        self._update_(key)

    def __repr__(self):
        return '<User Key [{0}]>'.format(self._title)

    def _update_(self, key):
        self._json_data = key
        self._api = key.get('url')
        self._id = key.get('id')
        self._title = key.get('title')
        self._key = key.get('key')

    def delete(self):
        """Delete this Key"""
        return self._boolean(self._delete(self._api), 204, 404)

    @property
    def key(self):
        """The text of the actual key"""
        return self._key

    @property
    def id(self):
        """The unique id of the key at GitHub"""
        return self._id

    @property
    def title(self):
        """The title the user gave to the key"""
        return self._title

    @GitHubCore.requires_auth
    def update(self, title, key):
        """Update this key.

        :param title: (required), title of the key
        :type title: str
        :param key: (required), text of the key file
        :type key: str
        :returns: bool
        """
        if not title:
            title = self._title
        if not key:
            key = self._key

        data = dumps({'title': title, 'key': key})
        json = self._json(self._patch(self._api, data), 200)

        if json:
            self._update_(json)
            return True
        return False


class Plan(GitHubObject):
    """The :class:`Plan <Plan>` object. This makes interacting with the plan
    information about a user easier.
    """
    def __init__(self, plan):
        super(Plan, self).__init__(plan)
        self._collab = plan.get('collaborators')
        self._name = plan.get('name')
        self._private = plan.get('private_repos')
        self._space = plan.get('space')

    def __repr__(self):
        return '<Plan [{0}]>'.format(self._name)

    @property
    def collaborators(self):
        """Number of collaborators"""
        return self._collab

    def is_free(self):
        """Checks if this is a free plan.

        :returns: bool
        """
        return self._name == 'free'

    @property
    def name(self):
        """Name of the plan"""
        return self._name

    @property
    def private_repos(self):
        """Number of private repos"""
        return self._private

    @property
    def space(self):
        """Space allowed"""
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
    """The :class:`User <User>` object. This handles and structures information
    in the `User section <http://developer.github.com/v3/users/>`_.
    """
    def __init__(self, user, session=None):
        super(User, self).__init__(user, session)
        self._update_(user)
        if not self._type:
            self._type = 'User'

    def __repr__(self):
        return '<User [{0}:{1}]>'.format(self._login, self._name)

    def _update_(self, user):
        # Private information
        super(User, self)._update_(user)
        if user.get('plan'):
            _plan = user.get('plan')
            self._plan = plans[_plan['name'].lower()]
            self._plan._space = _plan['space']
        else:
            self._plan = None

    @GitHubCore.requires_auth
    def add_email_addresses(self, addresses=[]):
        """Add the email addresses in ``addresses`` to the authenticated
        user's account.

        :param addresses: (optional), email addresses to be added
        :type addresses: list
        :returns: list of email addresses
        """
        json = []
        if addresses:
            url = self._build_url('user', 'emails')
            json = self._json(self._post(url, dumps(addresses)), 201)
        return json

    @GitHubCore.requires_auth
    def delete_email_addresses(self, addresses=[]):
        """Delete the email addresses in ``addresses`` from the
        authenticated user's account.

        :param addresses: (optional), email addresses to be removed
        :type addresses: list
        :returns: bool
        """
        url = self._build_url('user', 'emails')
        return self._boolean(self._delete(url, dumps(addresses)), 204, 404)

    @property
    def disk_usage(self):
        """How much disk consumed by the user"""
        return self._disk

    @property
    def for_hire(self):
        """True -- for hire, False -- not for hire"""
        return self._hire

    def is_assignee_on(self, login, repository):
        """Checks if this user can be assigned to issues on login/repository.

        :returns: :class:`bool`
        """
        url = self._build_url('repos', login, repository, 'assignees',
                self.login)
        return self._boolean(self._get(url), 204, 404)

    def list_events(self, public=False):
        """Events performed by this user.

        :param public: (optional), only list public events for the
            authenticated user
        :type public: bool
        :returns: list of :class:`Event <github3.event.Event>`\ s
        """
        # Paginate
        path = ['events']
        if public:
            path.append('public')
        url = self._build_url(*path, base_url=self._api)
        json = self._json(self._get(url), 200)
        return [Event(e, self) for e in json]

    def list_followers(self):
        """List followers of this user.

        :returns: list of :class:`User <User>`\ s
        """
        # Paginate
        url = self._build_url('followers', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [User(u, self) for u in json]

    def list_following(self):
        """List users being followed by this user.

        :returns: list of :class:`User <User>`\ s
        """
        # Paginate
        url = self._build_url('following', base_url=self._api)
        json = self._json(self._get(url), 200)
        return [User(u, self) for u in json]

    def list_org_events(self, org):
        """List events as they appear on the user's organization dashboard.
        You must be authenticated to view this.

        :param org: (required), name of the organization
        :type org: str
        :returns: list of :class:`Event <github3.event.Event>`\ s
        """
        # Paginate
        json = []
        if org:
            url = self._build_url('events', 'orgs', org, base_url=self._api)
            json = self._json(self._get(url), 200)
        return [Event(e, self) for e in json]

    def list_received_events(self, public=False):
        """List events that the user has received. If the user is the
        authenticated user, you will see private and public events, otherwise
        you will only see public events.

        :param public: (optional), determines if the authenticated user sees
            both private and public or just public
        :type public: bool
        :returns: list of :class:`Event <github3.event.Event>`\ s
        """
        # Paginate
        path = ['received_events']
        if public:
            path.append('public')
        url = self._build_url(*path, base_url=self._api)
        json = self._json(self._get(url), 200)
        return [Event(e, self) for e in json]

    @property
    def owned_private_repos(self):
        """Number of private repos owned by this user"""
        return self._owned_private_repos

    @property
    def private_gists(self):
        """Number of private gists owned by this user"""
        return self._private_gists

    @property
    def plan(self):
        """Which plan this user is on"""
        return self._plan

    @property
    def public_gists(self):
        """Number of public gists"""
        return self._public_gists

    @property
    def total_private_repos(self):
        """Total number of private repos"""
        return self._private_repos

    @GitHubCore.requires_auth
    def update(self, name=None, email=None, blog=None, company=None,
            location=None, hireable=False, bio=None):
        """If authenticated as this user, update the information with
        the information provided in the parameters.

        :param name: e.g., 'John Smith', not login name
        :type name: str
        :param email: e.g., 'john.smith@example.com'
        :type email: str
        :param blog: e.g., 'http://www.example.com/jsmith/blog'
        :type blog: str
        :param company:
        :type company: str
        :param location:
        :type location: str
        :param hireable: defaults to False
        :type hireable: bool
        :param bio: GitHub flavored markdown
        :type bio: str
        :returns: bool
        """
        user = dumps({'name': name, 'email': email, 'blog': blog,
            'company': company, 'location': location,
            'hireable': hireable, 'bio': bio})
        url = self._build_url('user')
        json = self._json(self._patch(url, user), 200)
        if json:
            self._update_(json)
            return True
        return False
