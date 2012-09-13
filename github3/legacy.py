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
        #: id of the gravatar account
        self.gravatar_id = issue.get('gravatar_id', '')
        #: Position
        self.position = issue.get('position', 0)
        #: Issue number
        self.number = issue.get('number', 0)
        #: Number of votes on this issue. Probably effectively deprecated
        self.votes = issue.get('votes', 0)
        #: datetime object representing the creation of the issue
        self.created_at = None
        if issue.get('created_at'):
            created = issue.get('created_at')[:-6] + 'Z'
            self.created_at = self._strptime(created)

        #: datetime object representing the last time the issue was updated
        self.updated_at = None
        if issue.get('updated_at'):
            updated = issue.get('updated_at')[:-6] + 'Z'
            self.updated_at = self._strptime(updated)
        #: Number of comments on the issue
        self.comments = issue.get('comments', 0)
        #: Body of the issue
        self.body = issue.get('body', '')
        #: Title of the issue
        self.title = issue.get('title', '')
        #: URL of the issue
        self.html_url = issue.get('html_url', '')
        #: User's login
        self.user = issue.get('user', '')
        #: list of labels applied to this issue
        self.labels = issue.get('labels', [])
        #: State of the issue, i.e., open or closed
        self.state = issue.get('state', '')

    def __repr__(self):
        return '<Legacy Issue [{0}:{1}]>'.format(self.user, self.number)


class LegacyRepo(GitHubCore):
    """The :class:`LegacyRepo <LegacyRepo>` object. This wraps data returned
    using the :func:`search_repos <github3.github.GitHub.search_repos>`"""
    def __init__(self, repo, session=None):
        super(LegacyRepo, self).__init__(repo, session)
        #: datetime object representing the date of creation of this repo
        self.created_at = None
        if repo.get('created'):
            created = repo.get('created')[:-6] + 'Z'
            self.created_at = self._strptime(created)
        #: datetime object representing the date of creation of this repo
        self.created = self.created_at
        #: description of this repository
        self.description = repo.get('description', '')
        #: Number of followers
        self.followers = repo.get('followers', 0)
        self._fork = repo.get('fork', False)
        #: Number of forks of this repository
        self.forks = repo.get('forks', 0)
        self._has_dl = repo.get('has_downloads', False)
        self._has_is = repo.get('has_issues', False)
        self._has_w = repo.get('has_wiki', False)
        #: URL of the website for this repository
        self.homepage = repo.get('homepage', '')
        #: Language used in this repository
        self.language = repo.get('language', '')
        #: Name of this repository
        self.name = repo.get('name', '')
        #: Number of open issues
        self.open_issues = repo.get('open_issues', 0)
        #: Owner of this repository
        self.owner = repo.get('owner', '')
        self._priv = repo.get('private', False)
        #: datetime object representing the last time the repo was pushed to
        self.pushed = None
        if repo.get('pushed_at'):
            pushed = repo.get('pushed_at')[:-6] + 'Z'  # (No coverage)
            self.pushed = self._strptime(pushed)  # (No coverage)
        #: datetime object representing the last time the repo was pushed to
        self.pushed_at = self.pushed
        #: Score
        self.score = repo.get('score', 0.0)
        #: Size of the repo
        self.size = repo.get('size', 0)
        #: Type of object
        self.type = repo.get('type', 'repo')
        #: User's login
        self.user = repo.get('username', '')
        #: URL of the project on GitHub
        self.url = repo.get('url', '')
        #: Number of people watching this project
        self.watchers = repo.get('watchers', 0)

    def __repr__(self):
        return '<Legacy Repo [{0}/{1}]>'.format(self.owner, self.name)

    def has_downloads(self):
        """Checks if this repository has downloads"""
        return self._has_dl

    def has_issues(self):
        """Checks if this repository has issues"""
        return self._has_is

    def has_wiki(self):
        """Checks if this repository has a wiki"""
        return self._has_w

    def is_fork(self):
        """Checks if this repository is a fork"""
        return self._fork

    def is_private(self):
        """Checks if this repository is private"""
        return self._priv


class LegacyUser(GitHubCore):
    """The :class:`LegacyUser <LegacyUser>` object. This handles information
    returned by :func:`search_users <github3.github.GitHub.search_users>`.
    """
    def __init__(self, user, session=None):
        super(LegacyUser, self).__init__(user, session)
        #: datetime object representing when the account was created
        self.created = None
        if user.get('created'):
            created = user.get('created')
            if not match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$', created):
                created = created[:-6] + 'Z'
            self.created = self._strptime(created)
        #: datetime object representing when the account was created
        self.created_at = self.created

        # same as followers_count
        #: Number of followers
        self.followers = user.get('followers', 0)
        #: Number of followers
        self.followers_count = self.followers
        #: Full name of this user
        self.fullname = user.get('fullname', '')
        #: Gravatar id for this user
        self.gravatar_id = user.get('gravatar_id', '')
        #: Unique id of this user
        self.id = user.get('id', '')
        #: Language
        self.language = user.get('language', '')
        #: Location of this user
        self.location = user.get('location', '')
        #: username for the user
        self.login = user.get('login', '')
        #: Full name of this user
        self.name = user.get('fullname', '')
        #: Number of public repos owned by this user
        self.public_repo_count = user.get('public_repo_count', 0)
        #: datetime representing the last time this user pushed
        self.pushed = None
        if user.get('pushed'):
            pushed = user.get('pushed')[:-5] + 'Z'  # (No coverage)
            self.pushed = self._strptime(pushed)  # (No coverage)
        #: datetime representing the last time this user pushed
        self.pushed_at = self.pushed
        #: User's record
        self.record = user.get('record', '')
        #: Number of repos owned by the user
        self.repos = user.get('repos', 0)
        #: Score
        self.score = user.get('score', 0.0)
        #: Type of user
        self.type = user.get('type', 'user')
        # username: same as login

    def __repr__(self):
        return '<Legacy User [{0}]>'.format(self.login)
