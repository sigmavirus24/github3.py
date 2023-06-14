"""
github3.actions
=============

Module which contains all GitHub Actions related material (only secrets
so far).

See also: http://developer.github.com/v3/actions/
"""
from .secrets import (
    OrganizationSecret,
    RepositorySecret,
    SharedOrganizationSecret,
)

__all__ = (
    "OrganizationSecret",
    "RepositorySecret",
    "SharedOrganizationSecret",
)
