"""
github3.utils
==================

This module provides internal utility classes and functions to the rest of the library

"""


class RequestsRawWrapper(object):
    """
    A recent change to requests (between 1.2.0 and 1.2.1) expected the
    `raw` field of a response object to be a urllib3 response object,
    breaking the compatability with 'file-like' objects. This wrapper
    discards the additional parameter now expected by requests in order
    to use file-like objects for the tests.

    See https://github.com/kennethreitz/requests/issues/1406
    """
    def __init__(self, wrapped_object):
        self._wrapped_object = wrapped_object

    def read(self, size=None, decode_content=False):
        return self._wrapped_object.read(size)