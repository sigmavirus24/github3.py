# -*- coding: utf-8 -*-
"""
github3.users
=============

This module contains everything relating to Users.

"""
from __future__ import unicode_literals

from json import dumps
from uritemplate import URITemplate
from github3.events import Event
from github3.models import GitHubObject, GitHubCore, BaseAccount
from github3.decorators import requires_auth


class Key(GitHubCore):
    """The :class:`Key <Key>` object. Please see GitHub's `Key Documentation
    <http://developer.github.com/v3/users/keys/>`_ for more information.

    Two key instances can be checked like so::

        k1 == k2
        k1 != k2

    And is equivalent to::

        k1.id == k2.id
        k1.id != k2.id
    """
    def __init__(self, key, session=None):
        super(Key, self).__init__(key, session)
        self._api = key.get('url', '')
        #: The text of the actual key
        self.key = key.get('key')
        #: The unique id of the key at GitHub
        self.id = key.get('id')
        #: The title the user gave to the key
        self.title = key.get('title')

    def _repr(self):
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
    information about a user easier. Please see GitHub's `Authenticated User
    <http://developer.github.com/v3/users/#get-the-authenticated-user>`_
    documentation for more specifics.
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

    def _repr(self):
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

    Two user instances can be checked like so::

        u1 == u2
        u1 != u2

    And is equivalent to::

        u1.id == u2.id
        u1.id != u2.id

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

        events_url = user.get('events_url', '')
        #: Events URL Template. Expands with ``privacy``
        self.events_urlt = URITemplate(events_url) if events_url else None

        #: Followers URL (not a template)
        self.followers_url = user.get('followers_url', '')

        furl = user.get('following_url', '')
        #: Following URL Template. Expands with ``other_user``
        self.following_urlt = URITemplate(furl) if furl else None

        gists_url = user.get('gists_url', '')
        #: Gists URL Template. Expands with ``gist_id``
        self.gists_urlt = URITemplate(gists_url) if gists_url else None

        #: Organizations URL (not a template)
        self.organizations_url = user.get('organizations_url', '')

        #: Received Events URL (not a template)
        self.received_events_url = user.get('received_events_url', '')

        #: Repostories URL (not a template)
        self.repos_url = user.get('repos_url', '')

        starred_url = user.get('starred_url', '')
        #: Starred URL Template. Expands with ``owner`` and ``repo``
        self.starred_urlt = URITemplate(starred_url) if starred_url else None

        #: Subscriptions URL (not a template)
        self.subscriptions_url = user.get('subscriptions_url', '')

        self._uniq = user.get('id', None)

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

    def is_following(self, login):
        """Checks if this user is following ``login``.

        :param str login: (required)
        :returns: bool

        """
        url = self.following_urlt.expand(other_user=login)
        return self._boolean(self._get(url), 204, 404)

    def iter_events(self, public=False, number=-1, etag=None):
        """Iterate over events performed by this user.

        :param bool public: (optional), only list public events for the
            authenticated user
        :param int number: (optional), number of events to return. Default: -1
            returns all available events.
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: list of :class:`Event <github3.events.Event>`\ s
        """
        path = ['events']
        if public:
            path.append('public')
        url = self._build_url(*path, base_url=self._api)
        return self._iter(int(number), url, Event, etag=etag)

    def iter_followers(self, number=-1, etag=None):
        """Iterate over the followers of this user.

        :param int number: (optional), number of followers to return. Default:
            -1 returns all available
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`User <User>`\ s
        """
        url = self._build_url('followers', base_url=self._api)
        return self._iter(int(number), url, User, etag=etag)

    def iter_following(self, number=-1, etag=None):
        """Iterate over the users being followed by this user.

        :param int number: (optional), number of users to return. Default: -1
            returns all available users
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`User <User>`\ s
        """
        url = self._build_url('following', base_url=self._api)
        return self._iter(int(number), url, User, etag=etag)

    def iter_keys(self, number=-1, etag=None):
        """Iterate over the public keys of this user.

        .. versionadded:: 0.5

        :param int number: (optional), number of keys to return. Default: -1
            returns all available keys
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Key <Key>`\ s
        """
        url = self._build_url('keys', base_url=self._api)
        return self._iter(int(number), url, Key, etag=etag)

    def iter_org_events(self, org, number=-1, etag=None):
        """Iterate over events as they appear on the user's organization
        dashboard. You must be authenticated to view this.

        :param str org: (required), name of the organization
        :param int number: (optional), number of events to return. Default: -1
            returns all available events
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: list of :class:`Event <github3.events.Event>`\ s
        """
        url = ''
        if org:
            url = self._build_url('events', 'orgs', org, base_url=self._api)
        return self._iter(int(number), url, Event, etag=etag)

    def iter_received_events(self, public=False, number=-1, etag=None):
        """Iterate over events that the user has received. If the user is the
        authenticated user, you will see private and public events, otherwise
        you will only see public events.

        :param bool public: (optional), determines if the authenticated user
            sees both private and public or just public
        :param int number: (optional), number of events to return. Default: -1
            returns all events available
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Event <github3.events.Event>`\ s
        """
        path = ['received_events']
        if public:
            path.append('public')
        url = self._build_url(*path, base_url=self._api)
        return self._iter(int(number), url, Event, etag=etag)

    def iter_orgs(self, number=-1, etag=None):
        """Iterate over organizations the user is member of

        :param int number: (optional), number of organizations to return.
            Default: -1 returns all available organization
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: list of :class:`Event <github3.orgs.Organization>`\ s
        """
        # Import here, because a toplevel import causes an import loop
        from github3.orgs import Organization
        url = self._build_url('orgs', base_url=self._api)
        return self._iter(int(number), url, Organization, etag=etag)

    def iter_starred(self, sort=None, direction=None, number=-1, etag=None):
        """Iterate over repositories starred by this user.

        .. versionchanged:: 0.5
           Added sort and direction parameters (optional) as per the change in
           GitHub's API.

        :param int number: (optional), number of starred repos to return.
            Default: -1, returns all available repos
        :param str sort: (optional), either 'created' (when the star was
            created) or 'updated' (when the repository was last pushed to)
        :param str direction: (optional), either 'asc' or 'desc'. Default:
            'desc'
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Repository <github3.repos.Repository>`
        """
        from github3.repos import Repository

        params = {'sort': sort, 'direction': direction}
        self._remove_none(params)
        url = self.starred_urlt.expand(owner=None, repo=None)
        return self._iter(int(number), url, Repository, params, etag)

    def iter_subscriptions(self, number=-1, etag=None):
        """Iterate over repositories subscribed to by this user.

        :param int number: (optional), number of subscriptions to return.
            Default: -1, returns all available
        :param str etag: (optional), ETag from a previous request to the same
            endpoint
        :returns: generator of :class:`Repository <github3.repos.Repository>`
        """
        from github3.repos import Repository
        url = self._build_url('subscriptions', base_url=self._api)
        return self._iter(int(number), url, Repository, etag=etag)

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
