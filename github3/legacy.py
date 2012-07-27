"""
github3.legacy
==============

This module contains legacy objects for use with the Search_ section of the
API.

.. _Search: http://developer.github.com/v3/search/

"""

from .models import GitHubCore
from re import match


class LegacyIssue(GitHubCore):
    """The :class:`LegacyIssue <LegacyIssue>` object. This object is only
    every used in conjuction with the :func:`search_issues
    <github3.github.GitHub.search_issues>`. Unfortunately, GitHub hasn't
    updated the search functionality to use the objects as they exist now.
    """
    def __init__(self, issue, session=None):
        super(LegacyIssue, self).__init__(issue, session)
        self._gravid = issue.get('gravatar_id', '')
        self._pos = issue.get('position', 0)
        self._num = issue.get('number', 0)
        self._votes = issue.get('votes', 0)
        self._created = None
        if issue.get('created_at'):
            created = issue.get('created_at')[:-6] + 'Z'
            self._created = self._strptime(created)
        self._updated = None
        if issue.get('updated_at'):
            updated = issue.get('updated_at')[:-6] + 'Z'
            self._updated = self._strptime(updated)
        self._comments = issue.get('comments', 0)
        self._body = issue.get('body', '')
        self._title = issue.get('title', '')
        self._html = issue.get('html_url', '')
        self._user = issue.get('user', '')
        self._labels = issue.get('labels', [])
        self._state = issue.get('state', '')

    def __repr__(self):
        return '<Legacy Issue [{0}:{1}]>'.format(self._user, self._num)

    @property
    def body(self):
        """Body of the issue"""
        return self._body

    @property
    def comments(self):
        """Number of comments on the issue"""
        return self._comments

    @property
    def created_at(self):
        """datetime object representing the creation of the issue"""
        return self._created

    @property
    def gravatar_id(self):
        """id of the gravatar account"""
        return self._gravid

    @property
    def html_url(self):
        """URL of the issue"""
        return self._html

    @property
    def labels(self):
        """list of labels applied to this issue"""
        return self._labels

    @property
    def number(self):
        """Issue number"""
        return self._num

    @property
    def position(self):
        """Position"""
        return self._pos

    @property
    def state(self):
        """State of the issue, i.e., open or closed"""
        return self._state

    @property
    def title(self):
        """Title of the issue"""
        return self._title

    @property
    def updated_at(self):
        """datetime object representing the last time the issue was updated"""
        return self._updated

    @property
    def user(self):
        """User's login"""
        return self._user

    @property
    def votes(self):
        """Number of votes on this issue. Probably effectively deprecated"""
        return self._votes


class LegacyRepo(GitHubCore):
    """The :class:`LegacyRepo <LegacyRepo>` object. This wraps data returned
    using the :func:`search_repos <github3.github.GitHub.search_repos>`"""
    def __init__(self, repo, session=None):
        super(LegacyRepo, self).__init__(repo, session)
        self._created = None
        if repo.get('created'):
            created = repo.get('created')[:-6] + 'Z'
            self._created = self._strptime(created)
        self._desc = repo.get('description', '')
        self._followers = repo.get('followers', 0)
        self._fork = repo.get('fork', False)
        self._forks = repo.get('forks', 0)
        self._has_dl = repo.get('has_downloads', False)
        self._has_is = repo.get('has_issues', False)
        self._has_w = repo.get('has_wiki', False)
        self._home = repo.get('homepage', '')
        self._lang = repo.get('language', '')
        self._name = repo.get('name', '')
        self._open = repo.get('open_issues', 0)
        self._owner = repo.get('owner', '')
        self._priv = repo.get('private', False)
        self._pushed = None
        if repo.get('pushed_at'):
            pushed = repo.get('pushed_at')[:-6] + 'Z'
            self._pushed = self._strptime(pushed)
        self._score = repo.get('score', 0.0)
        self._sz = repo.get('size', 0)
        self._type = repo.get('type', 'repo')
        self._user = repo.get('username', '')
        self._url = repo.get('url', '')
        self._watchers = repo.get('watchers', 0)

    def __repr__(self):
        return '<Legacy Repo [{0}/{1}]>'.format(self._owner, self._name)

    @property
    def created(self):
        """datetime object representing the date of creation of this repo"""
        return self._created

    @property
    def created_at(self):
        """datetime object representing the date of creation of this repo"""
        return self._created

    @property
    def description(self):
        """description of this repository"""
        return self._desc

    @property
    def followers(self):
        """Number of followers"""
        return self._followers

    @property
    def forks(self):
        """Number of forks of this repository"""
        return self._forks

    def has_downloads(self):
        """Checks if this repository has downloads"""
        return self._has_dl

    def has_issues(self):
        """Checks if this repository has issues"""
        return self._has_is

    def has_wiki(self):
        """Checks if this repository has a wiki"""
        return self._has_w

    @property
    def homepage(self):
        """URL of the website for this repository"""
        return self._home

    def is_fork(self):
        """Checks if this repository is a fork"""
        return self._fork

    @property
    def language(self):
        """Language used in this repository"""
        return self._lang

    @property
    def name(self):
        """Name of this repository"""
        return self._name

    @property
    def open_issues(self):
        """Number of open issues"""
        return self._open

    @property
    def owner(self):
        """Owner of this repository"""
        return self._owner

    def is_private(self):
        """Checks if this repository is private"""
        return self._priv

    @property
    def pushed(self):
        """datetime object representing the last time the repo was pushed to"""
        return self._pushed

    @property
    def pushed_at(self):
        """datetime object representing the last time the repo was pushed to"""
        return self._pushed

    @property
    def score(self):
        """Score"""
        return self._score

    @property
    def size(self):
        """Size of the repo"""
        return self._sz

    @property
    def type(self):
        """Type of object"""
        return self._type

    @property
    def user(self):
        """User"""
        return self._user

    @property
    def url(self):
        """URL of the project on GitHub"""
        return self._url

    @property
    def watchers(self):
        """Number of people watching this project"""
        return self._watchers


class LegacyUser(GitHubCore):
    """The :class:`LegacyUser <LegacyUser>` object. This handles information
    returned by :func:`search_users <github3.github.GitHub.search_users>`.
    """
    def __init__(self, user, session=None):
        super(LegacyUser, self).__init__(user, session)
        self._created = None
        if user.get('created'):
            created = user.get('created')
            if not match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$', created):
                created = created[:-6] + 'Z'
            self._created = self._strptime(created)
        self._followers = user.get('followers', 0)
        # same as followers_count
        self._fullname = user.get('fullname', '')
        self._gravid = user.get('gravatar_id', '')
        self._id = user.get('id', '')
        self._lang = user.get('language', '')
        self._loc = user.get('location', '')
        self._login = user.get('login', '')
        # name: same as fullname
        self._pubrepo = user.get('public_repo_count', 0)
        self._pushed = None
        if user.get('pushed'):
            pushed = user.get('pushed')[:-5] + 'Z'
            self._pushed = self._strptime(pushed)
        self._rec = user.get('record', '')
        self._repos = user.get('repos', 0)
        self._score = user.get('score', 0.0)
        self._type = user.get('type', 'user')
        # username: same as login

    def __repr__(self):
        return '<Legacy User [{0}]>'.format(self._login)

    @property
    def created(self):
        """datetime object representing when the account was created"""
        return self._created

    @property
    def created_at(self):
        """datetime object representing when the account was created"""
        return self._created

    @property
    def followers(self):
        """Number of followers"""
        return self._followers

    @property
    def followers_count(self):
        """Number of followers"""
        return self._followers

    @property
    def fullname(self):
        """Full name of this user"""
        return self._fullname

    @property
    def gravatar_id(self):
        """Gravatar id for this user"""
        return self._gravid

    @property
    def id(self):
        """Unique id of this user"""
        return self._id

    @property
    def language(self):
        """Language"""
        return self._lang

    @property
    def location(self):
        """Location of this user"""
        return self._loc

    @property
    def login(self):
        """username for the user"""
        return self._login

    @property
    def name(self):
        """Full name of the user"""
        return self._fullname

    @property
    def public_repo_count(self):
        """Number of public repos owned by this user"""
        return self._pubrepo

    @property
    def pushed(self):
        """datetime representing the last time this user pushed"""
        return self._pushed

    @property
    def record(self):
        """User's record"""
        return self._rec

    @property
    def repos(self):
        """Number of repos owned by the user"""
        return self._repos

    @property
    def score(self):
        """Score"""
        return self._score

    @property
    def type(self):
        """Type of user"""
        return self._type
