"""
github3.repos
=============

This module contains the classes relating to repositories.

See also: http://developer.github.com/v3/repos/
"""

from .repo import Repository, ShortRepository, StarredRepository

__all__ = ("Repository", "ShortRepository", "StarredRepository")
