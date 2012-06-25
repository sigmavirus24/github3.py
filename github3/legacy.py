"""
github3.legacy
==============

This module contains legacy objects for use with the Search_ section of the 
API.

.. _Search: http://developer.github.com/v3/search/

"""

from .models import GitHubCore
from .issue import Issue
from .repo import Repository

class LegacyIssue(GitHubCore):
    pass
