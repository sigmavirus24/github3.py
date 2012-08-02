"""
github3
=======

See http://github3py.rtfd.org/ for documentation.

:copyright: (c) 2012 by Ian Cordasco
:license: Modified BSD, see LICENSE for more details

"""

__title__ = 'github3'
__author__ = 'Ian Cordasco'
__license__ = 'Modified BSD'
__copyright__ = 'Copyright 2012 Ian Cordasco'
__version__ = '0.1a5'

from .api import *
from .github import GitHub
from .models import GitHubError
from .event import Event
from .gist import Gist, GistComment, GistFile
from .git import Blob, GitData, Commit, Reference, GitObject, Tag, Tree, Hash
from .issue import Issue, IssueComment, IssueEvent, Label, Milestone
from .legacy import LegacyUser, LegacyRepo, LegacyIssue
from .org import Organization, Team
from .pulls import PullRequest
from .repo import Repository, Branch
from .user import User
