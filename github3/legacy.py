"""
github3.legacy
==============

This module contains legacy objects for use with the Search_ section of the 
API.

.. _Search: http://developer.github.com/v3/search/

"""

from .models import GitHubCore

class LegacyIssue(GitHubCore):
    """The :class:`LegacyIssue <LegacyIssue>` object. This object is only every
    used in conjuction with the :func:`search_issues
    <github.Github.search_issues>`. Unfortunately, GitHub hasn't updated the
    search functionality to use the objects as they exist now.
    """
    def __init__(self, issue, session):
        super(LegacyIssue, self).__init__(session)
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
        return '<Legacy Issue [%s:%s]>' % (self._user, self._num)

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
