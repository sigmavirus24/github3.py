# -*- coding: utf-8 -*-
"""
github3
=======

See https://github3.readthedocs.io/ for documentation.

:copyright: (c) 2012-2016 by Ian Cordasco
:license: Modified BSD, see LICENSE for more details

"""

from .__about__ import (
    __package_name__,
    __title__,
    __author__,
    __author_email__,
    __license__,
    __copyright__,
    __version__,
    __version_info__,
    __url__,
)
from .api import (
    all_events,
    all_repositories,
    all_users,
    authorize,
    create_gist,
    emojis,
    enterprise_login,
    followed_by,
    followers_of,
    gist,
    gists_by,
    gitignore_template,
    gitignore_templates,
    issue,
    issues_on,
    login,
    markdown,
    octocat,
    organization,
    organizations_with,
    public_gists,
    pull_request,
    rate_limit,
    repositories_by,
    repository,
    search_code,
    search_issues,
    search_repositories,
    search_users,
    starred_by,
    subscriptions_for,
    user,
    zen,
)
from .github import GitHub, GitHubEnterprise, GitHubStatus
from .exceptions import GitHubError

__all__ = (
    "GitHub",
    "GitHubEnterprise",
    "GitHubError",
    "GitHubStatus",
    "authorize",
    "login",
    "enterprise_login",
    "emojis",
    "gist",
    "gitignore_template",
    "create_gist",
    "issue",
    "markdown",
    "octocat",
    "organization",
    "pull_request",
    "followers_of",
    "followed_by",
    "public_gists",
    "gists_by",
    "issues_on",
    "gitignore_templates",
    "all_repositories",
    "all_users",
    "all_events",
    "organizations_with",
    "repositories_by",
    "starred_by",
    "subscriptions_for",
    "rate_limit",
    "repository",
    "search_code",
    "search_repositories",
    "search_users",
    "search_issues",
    "user",
    "zen",
    # Metadata attributes
    "__package_name__",
    "__title__",
    "__author__",
    "__author_email__",
    "__license__",
    "__copyright__",
    "__version__",
    "__version_info__",
    "__url__",
)
