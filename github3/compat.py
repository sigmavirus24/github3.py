"""
github3.compat
==============

This module handles any any compatibility issues across versions of python.

"""

from sys import version_info
from json import loads as jloads


def loads(data):
    """If we're dealing with python 3000, decode the data first, then load it
    using the json module."""

    if version_info >= (3, 0):
        data = data.decode('utf-8')

    return jloads(data)
