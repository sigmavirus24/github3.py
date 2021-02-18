"""github4.py."""
import sys

if sys.version_info[:2] >= (3, 8):
    from importlib.metadata import version, PackageNotFoundError  # pragma: no cover
else:
    from importlib_metadata import version, PackageNotFoundError  # pragma: no cover

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from .api import enterprise_login
from .api import login
from .exceptions import GitHubError
from .github import GitHub
from .github import GitHubEnterprise

__all__ = (
    "GitHub",
    "GitHubEnterprise",
    "GitHubError",
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
)
