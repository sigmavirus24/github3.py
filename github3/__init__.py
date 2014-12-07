# -*- coding: utf-8 -*-
"""
github3
=======

See http://github3py.rtfd.org/ for documentation.

:copyright: (c) 2012-2014 by Ian Cordasco
:license: Modified BSD, see LICENSE for more details

"""

__title__ = 'github3'
__author__ = 'Ian Cordasco'
__license__ = 'Modified BSD'
__copyright__ = 'Copyright 2012-2014 Ian Cordasco'
__version__ = '1.0.0a1'
__version_info__ = tuple(int(i) for i in __version__.split('.') if i.isdigit())

from .api import (
    authorize, login, enterprise_login, emojis, gist, gitignore_template,
    create_gist, issue, markdown, octocat, organization, pull_request,
    followers_of, followed_by, public_gists, gists_by, issues_on,
    gitignore_templates, all_repositories, all_users, all_events,
    organizations_with, repositories_by, starred_by, subscriptions_for,
    rate_limit, repository, search_code, search_repositories, search_users,
    user, zen
)
from .github import GitHub, GitHubEnterprise, GitHubStatus
from .exceptions import (
    BadRequest, AuthenticationFailed, ForbiddenError, GitHubError,
    MethodNotAllowed, NotFoundError, ServerError, NotAcceptable,
    UnprocessableEntity
)

__all__ = (
    'AuthenticationFailed',  'BadRequest', 'ForbiddenError', 'GitHub',
    'GitHubEnterprise', 'GitHubError', 'GitHubStatus', 'InvalidRequestError',
    'MethodNotAllowed', 'NotAcceptable', 'NotFoundError', 'ServerError',
    'UnprocessableEntity', 'authorize', 'login', 'enterprise_login', 'emojis',
    'gist', 'gitignore_template', 'create_gist', 'issue', 'markdown',
    'octocat', 'organization', 'pull_request', 'followers_of', 'followed_by',
    'public_gists', 'gists_by', 'issues_on', 'gitignore_templates',
    'all_repositories', 'all_users', 'all_events', 'organizations_with',
    'repositories_by', 'starred_by', 'subscriptions_for', 'rate_limit',
    'repository', 'search_code', 'search_repositories', 'search_users',
    'user', 'zen',
)
