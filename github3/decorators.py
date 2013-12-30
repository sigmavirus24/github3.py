# -*- coding: utf-8 -*-
"""
github3.decorators
==================

This module provides decorators to the rest of the library

"""

from functools import wraps
from requests.models import Response
import os

try:  # (No coverage)
    # python2
    from StringIO import StringIO  # (No coverage)
except ImportError:  # (No coverage)
    # python3
    from io import BytesIO as StringIO


class RequestsStringIO(StringIO):
    def read(self, n=-1, *args, **kwargs):
        # StringIO is an old-style class, so can't use super
        return StringIO.read(self, n)


def requires_auth(func):
    """Decorator to note which object methods require authorization."""
    @wraps(func)
    def auth_wrapper(self, *args, **kwargs):
        auth = False
        if hasattr(self, '_session'):
            auth = (self._session.auth or
                    self._session.headers.get('Authorization'))

        if auth:
            return func(self, *args, **kwargs)
        else:
            from github3.models import GitHubError
            # Mock a 401 response
            r = generate_fake_error_response(
                '{"message": "Requires authentication"}'.encode()
            )
            raise GitHubError(r)
    return auth_wrapper


def requires_basic_auth(func):
    """Specific (basic) authentication decorator.

    This is used to note which object methods require username/password
    authorization and won't work with token based authorization.

    """
    @wraps(func)
    def auth_wrapper(self, *args, **kwargs):
        if hasattr(self, '_session') and self._session.auth:
            return func(self, *args, **kwargs)
        else:
            from github3.models import GitHubError
            # Mock a 401 response
            r = generate_fake_error_response(
                ('{"message": "Requires username/password authentication"}'
                 ).encode()
            )
            raise GitHubError(r)
    return auth_wrapper


def generate_fake_error_response(msg, status_code=401, encoding='utf-8'):
    r = Response()
    r.status_code = status_code
    r.encoding = encoding
    r.raw = RequestsStringIO(msg)
    r._content_consumed = True
    r._content = r.raw.read()
    return r

# Use mock decorators when generating documentation, so all functino signatures
# are displayed correctly
if os.getenv('GENERATING_DOCUMENTATION', None) == 'github3':
    requires_auth = requires_basic_auth = lambda x: x  # noqa  # (No coverage)
