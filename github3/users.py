"""
github3.users
=============

This module contains everything relating to Users.

"""

from json import dumps
from github3.events import Event
from github3.models import GitHubObject, GitHubCore, BaseAccount
from github3.decorators import requires_auth


class Key(GitHubCore):
    """The :class:`Key <Key>` object."""
    def __init__(self, key, session=None):
        super(Key, self).__init__(key, session)
        self._api = key.get('url', '')
        #: The text of the actual key
        self.key = key.get('key')
        #: The unique id of the key at GitHub
        self.id = key.get('id')
        #: The title the user gave to the key
        self.title = key.get('title')

    def __repr__(self):
        return '<User Key [{0}]>'.format(self.title)

    def __str__(self):
        return self.key

    def _update_(self, key):
        self.__init__(key, self._session)

    @requires_auth
    def delete(self):
        """Delete this Key"""
        return self._boolean(self._delete(self._api), 204, 404)

    @requires_auth
    def update(self, title, key):
        """Update this key.

        :param str title: (required), title of the key
        :param str key: (required), text of the key file
        :returns: bool
        """
        json = None
        if title and key:
            data = {'title': title, 'key': key}
            json = self._json(self._patch(self._api, data=dumps(data)), 200)
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
        #: Number of collaborators
        self.collaborators = plan.get('collaborators')
        #: Name of the plan
        self.name = plan.get('name')
        #: Number of private repos
        self.private_repos = plan.get('private_repos')
        #: Space allowed
        self.space = plan.get('space')

    def __repr__(self):
        return '<Plan [{0}]>'.format(self.name)  # (No coverage)

    def __str__(self):
        return self.name

    def is_free(self):
        """Checks if this is a free plan.

        :returns: bool
        """
        return self.name == 'free'  # (No coverage)


class User(BaseAccount):
    """The :class:`User <User>` object. This handles and structures information
    in the `User section <http://developer.github.com/v3/users/>`_.
    """
    def __init__(self, user, session=None):
        super(User, self).__init__(user, session)
        if not self.type:
            self.type = 'User'

        #: ID of the user's image on Gravatar
        self.gravatar_id = user.get('gravatar_id', '')
        #: True -- for hire, False -- not for hire
        self.hireable = user.get('hireable', False)

        ## The number of public_gists
        #: Number of public gists
        self.public_gists = user.get('public_gists', 0)

        # Private information
        #: How much disk consumed by the user
        self.disk_usage = user.get('disk_usage', 0)

        #: Number of private repos owned by this user
        self.owned_private_repos = user.get('owned_private_repos', 0)
        #: Number of private gists owned by this user
        self.total_private_gists = user.get('total_private_gists', 0)
        #: Total number of private repos
        self.total_private_repos = user.get('total_private_repos', 0)

        #: Which plan this user is on
        self.plan = Plan(user.get('plan', {}))

    def __repr__(self):
        return '<User [{0}:{1}]>'.format(self.login, self.name)

    def __str__(self):
        return self.login

    def _update_(self, user):
        self.__init__(user, self._session)

    @requires_auth
    def add_email_address(self, address):
        """Add the single email address to the authenticated user's
        account.

        :param str address: (required), email address to add
        :returns: list of email addresses
        """
        return self.add_email_addresses([address])

    @requires_auth
    def add_email_addresses(self, addresses=[]):
        """Add the email addresses in ``addresses`` to the authenticated
        user's account.

        :param list addresses: (optional), email addresses to be added
        :returns: list of email addresses
        """
        json = []
        if addresses:
            url = self._build_url('user', 'emails')
            json = self._json(self._post(url, data=addresses), 201)
        return json

    @requires_auth
    def delete_email_address(self, address):
        """Delete the email address from the user's account.

        :param str address: (required), email address to delete
        :returns: bool
        """
        return self.delete_email_addresses([address])

    @requires_auth
    def delete_email_addresses(self, addresses=[]):
        """Delete the email addresses in ``addresses`` from the
        authenticated user's account.

        :param list addresses: (optional), email addresses to be removed
        :returns: bool
        """
        url = self._build_url('user', 'emails')
        return self._boolean(self._delete(url, data=dumps(addresses)),
                             204, 404)

    def is_assignee_on(self, login, repository):
        """Checks if this user can be assigned to issues on login/repository.

        :returns: :class:`bool`
        """
        url = self._build_url('repos', login, repository, 'assignees',
                              self.login)
        return self._boolean(self._get(url), 204, 404)

    def iter_events(self, public=False, number=-1):
        """Iterate over events performed by this user.

        :param bool public: (optional), only list public events for the
            authenticated user
        :param int number: (optional), number of events to return. Default: -1
            returns all available events.
        :returns: list of :class:`Event <github3.events.Event>`\ s
        """
        path = ['events']
        if public:
            path.append('public')
        url = self._build_url(*path, base_url=self._api)
        return self._iter(int(number), url, Event)

    def iter_followers(self, number=-1):
        """Iterate over the followers of this user.

        :param int number: (optional), number of followers to return. Default:
            -1 returns all available
        :returns: generator of :class:`User <User>`\ s
        """
        url = self._build_url('followers', base_url=self._api)
        return self._iter(int(number), url, User)

    def iter_following(self, number=-1):
        """Iterate over the users being followed by this user.

        :param int number: (optional), number of users to return. Default: -1
            returns all available users
        :returns: generator of :class:`User <User>`\ s
        """
        url = self._build_url('following', base_url=self._api)
        return self._iter(int(number), url, User)

    def iter_keys(self, number=-1):
        """Iterate over the public keys of this user.

        :param int number: (optional), number of keys to return. Default: -1
            returns all available keys
        :returns: generator of :class:`Key <Key>`\ s
        """
        url = self._build_url('keys', base_url=self._api)
        return self._iter(int(number), url, Key)

    def iter_org_events(self, org, number=-1):
        """Iterate over events as they appear on the user's organization
        dashboard. You must be authenticated to view this.

        :param str org: (required), name of the organization
        :param int number: (optional), number of events to return. Default: -1
            returns all available events
        :returns: list of :class:`Event <github3.events.Event>`\ s
        """
        url = ''
        if org:
            url = self._build_url('events', 'orgs', org, base_url=self._api)
        return self._iter(int(number), url, Event)

    def iter_received_events(self, public=False, number=-1):
        """Iterate over events that the user has received. If the user is the
        authenticated user, you will see private and public events, otherwise
        you will only see public events.

        :param bool public: (optional), determines if the authenticated user
            sees both private and public or just public
        :param int number: (optional), number of events to return. Default: -1
            returns all events available
        :returns: generator of :class:`Event <github3.events.Event>`\ s
        """
        path = ['received_events']
        if public:
            path.append('public')
        url = self._build_url(*path, base_url=self._api)
        return self._iter(int(number), url, Event)

    def iter_starred(self, number=-1):
        """Iterate over repositories starred by this user.

        :param int number: (optional), number of starred repos to return.
            Default: -1, returns all available repos
        :returns: generator of :class:`Repository <github3.repos.Repository>`
        """
        from github3.repos import Repository
        url = self._build_url('starred', base_url=self._api)
        return self._iter(int(number), url, Repository)

    def iter_subscriptions(self, number=-1):
        """Iterate over repositories subscribed to by this user.

        :param int number: (optional), number of subscriptions to return.
            Default: -1, returns all available
        :returns: generator of :class:`Repository <github3.repos.Repository>`
        """
        from github3.repos import Repository
        url = self._build_url('subscriptions', base_url=self._api)
        return self._iter(int(number), url, Repository)

    @requires_auth
    def update(self, name=None, email=None, blog=None, company=None,
               location=None, hireable=False, bio=None):
        """If authenticated as this user, update the information with
        the information provided in the parameters.

        :param str name: e.g., 'John Smith', not login name
        :param str email: e.g., 'john.smith@example.com'
        :param str blog: e.g., 'http://www.example.com/jsmith/blog'
        :param str company:
        :param str location:
        :param bool hireable: defaults to False
        :param str bio: GitHub flavored markdown
        :returns: bool
        """
        user = {'name': name, 'email': email, 'blog': blog,
                'company': company, 'location': location,
                'hireable': hireable, 'bio': bio}
        self._remove_none(user)
        url = self._build_url('user')
        json = self._json(self._patch(url, data=dumps(user)), 200)
        if json:
            self._update_(json)
            return True
        return False
