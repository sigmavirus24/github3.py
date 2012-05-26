"""
github3.user
============

This module contains everything relating to Users.

"""

from json import dumps
from .compat import loads
from .models import GitHubCore


class Key(GitHubCore):
    def __init__(self, key, session):
        super(Key, self).__init__(session)
        self._update_(key)

    def __repr__(self):
        return '<User Key [%s]>' % self._title

    def _update_(self, key):
        self._api_url = key.get('url')
        self._id = key.get('id')
        self._title = key.get('title')
        self._key = key.get('key')

    def delete(self):
        resp = self._delete(self._api_url)
        if resp.status_code == 204:
            return True
        return False

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

        resp = self._patch(self._api_url, dumps({'title': title,
            'key': key}))
        if resp.status_code == 200:
            self._update_(loads(resp.content))
            return True
        return False


class Plan(object):
    def __init__(self, plan):
        super(Plan, self).__init__()
        self._collab = plan.get('collaborators')
        self._name = plan.get('name')
        self._private = plan.get('private_repos')
        self._space = plan.get('space')

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
    def __init__(self, user, session):
        super(User, self).__init__(session)
        self._update_(user)

    def __repr__(self):
        return '<User [%s:%s]>' % (self._login, self._name)

    def _update_(self, user):
        # Public information
        ## e.g. https://api.github.com/users/self._login
        self._api_url = user.get('url')

        self._avatar = user.get('avatar_url')
        self._bio = user.get('bio')
        self._blog = user.get('blog')
        self._company = user.get('company')

        self._created = None
        if user.get('created_at'):
            self._created = self._strptime(user.get('created_at'))
        self._email = user.get('email')

        ## The number of people following this user
        self._followers = user.get('followers')

        ## The number of people this user follows
        self._following = user.get('following')

        ## The number of people this user folows
        self._grav_id = user.get('gravatar_id')

        self._hire = user.get('hireable')
        self._id = user.get('id')
        self._location = user.get('location')
        self._login = user.get('login')

        ## e.g. first_name last_name
        self._name = user.get('name')

        ## The number of public_gists
        self._public_gists = user.get('public_gists')

        ## The number of public_repos
        self._public_repos = user.get('public_repos')

        ## e.g. https://github.com/self._login
        self._url = user.get('html_url')

        # Private information
        self._disk = user.get('disk_usage')
        if user.get('plan'):
            _plan = user.get('plan')
            self._plan = plans[_plan['name'].lower()]
            self._plan._space = _plan['space']
        else:
            self._plan = None

        ## The number of private repos
        self._private_repos = user.get('total_private_repos')
        self._private_gists = user.get('total_private_gists')

        self._owned_private_repos = user.get('owned_private_repos')

    def add_email_addresses(self, addresses=[]):
        """Add the email addresses in ``addresses`` to the authenticated 
        user's account."""
        if addresses:
            url = '/'.join([self._github_url, 'user', 'emails'])
            resp = self._post(url, dumps(addresses))
            if resp.status_code == 201:
                return loads(resp.content)
        return []

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
    def created_at(self):
        return self._created

    def delete_email_addresses(self, addresses=[]):
        """Delete the email addresses in ``addresses`` from the 
        authenticated user's account."""
        url = '/'.join([self._github_url, 'user', 'emails'])
        resp = self._delete(url, data=dumps(addresses))
        if resp.status_code == 204:
            return True
        return False

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

    def list_emails(self):
        """List email addresses for a user.
        
        Predicated on the assumption that you're authenticated for this  
        user.
        """
        url = '/'.join([self._github_url, 'user', 'emails'])
        resp = self._get(url)
        if resp.status_code == 200:
            return loads(resp.content)
        return []

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
        url = '/'.join([self._github_url, 'user'])
        resp = self._patch(url, user)
        if resp.status_code == 200:
            self._update_(loads(resp.content))
            return True
        return False
