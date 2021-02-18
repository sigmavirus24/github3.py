"""
github4.issues
==============

This module contains the classes related to issues.

See also: http://developer.github.com/v3/issues/
"""
import sys

from ..utils import timestamp_parameter
from .issue import Issue
from .issue import ShortIssue


if sys.version_info[:2] >= (3, 8):
    from importlib.metadata import version, PackageNotFoundError  # pragma: no cover
else:
    from importlib_metadata import version, PackageNotFoundError  # pragma: no cover

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

__all__ = ["Issue", "ShortIssue"]


def issue_params(filter, state, labels, sort, direction, since):
    params = {}
    if filter in ("assigned", "created", "mentioned", "subscribed", "all"):
        params["filter"] = filter

    if state in ("open", "closed", "all"):
        params["state"] = state

    if labels:
        params["labels"] = labels

    if sort in ("created", "updated", "comments"):
        params["sort"] = sort

    if direction in ("asc", "desc"):
        params["direction"] = direction

    since = timestamp_parameter(since)
    if since:
        params["since"] = since

    return params
