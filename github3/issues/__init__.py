"""
github3.issues
==============

This module contains the classes related to issues.

See also: http://developer.github.com/v3/issues/
"""

from re import match
from .issue import Issue

__all__ = [Issue]


def issue_params(filter, state, labels, sort, direction, since):
    params = {}
    if filter in ('assigned', 'created', 'mentioned', 'subscribed'):
        params['filter'] = filter

    if state in ('open', 'closed'):
        params['state'] = state

    if labels:
        params['labels'] = labels

    if sort in ('created', 'updated', 'comments'):
        params['sort'] = sort

    if direction in ('asc', 'desc'):
        params['direction'] = direction

    if since and match('\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$', since):
        params['since'] = since

    return params
