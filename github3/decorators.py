"""
github3.decorators
==================

This module provides decorators to the rest of the library

"""

from functools import wraps
from requests.models import Response

try:  # (No coverage)
    # python2
    from StringIO import StringIO  # (No coverage)
except ImportError:  # (No coverage)
    # python3
    from io import BytesIO as StringIO  # (No coverage)


def requires_auth(func):
    """Decorator to note which object methods require authorization.

    .. note::
        This decorator causes the wrapped methods to lose their proper
        signature. Please refer to the documentation for each of those.
    """
    #note = """.. note::
    #The signature of this function may not appear correctly in
    #documentation. Please adhere to the defined parameters and their
    #types.
    #"""
    ## Append the above note to each function this is applied to
    #func.__doc__ = '\n\n'.join([func.__doc__, note])

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
            r = Response()
            r.status_code = 401
            r.encoding = 'utf-8'
            r.raw = StringIO('{"message": "Requires authentication"}'.encode())
            raise GitHubError(r)
    return auth_wrapper
