"""
github3.models
==============

This module provides the basic models used in github3.py

"""

class GitHubCore(object):
    """A basic class for the other classes."""
    def __init__(self):
        self._session = None
        self._github_url = 'https://api.github.com'
        self._time_format = '%Y-%m-%dT%H:%M:%SZ'

    def __repr__(self):
        return '<github3-core at 0x%x>' % id(self)
