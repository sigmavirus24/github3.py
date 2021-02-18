"""
github4.gists
=============

Module which contains all the gist related material.

Sub-modules:
    github4.gists.gist
    github4.gists.file
    github4.gists.comment
    github4.gists.history

See also: http://developer.github.com/v3/gists/
"""
from .gist import Gist
from .gist import ShortGist

__all__ = ("Gist", "ShortGist")
