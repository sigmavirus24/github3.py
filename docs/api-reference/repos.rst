========================
 Repository API Objects
========================

This section of the documentation covers the representations of various
objects related to the `Repositories API`_.


Repository Objects
------------------

.. autoclass:: github4.repos.repo.Repository
    :inherited-members:

.. autoclass:: github4.repos.repo.ShortRepository
    :inherited-members:

.. autoclass:: github4.repos.repo.StarredRepository
    :inherited-members:

.. autoclass:: github4.repos.contents.Contents
    :members:

.. autoclass:: github4.repos.hook.Hook
    :members:

.. autoclass:: github4.repos.issue_import.ImportedIssue
    :members:


Git-related Objects
-------------------

.. autoclass:: github4.repos.tag.RepoTag
    :members:

Branches
~~~~~~~~

.. autoclass:: github4.repos.branch.Branch
    :members:

.. autoclass:: github4.repos.branch.ShortBranch
    :members:

.. autoclass:: github4.repos.branch.BranchProtection
    :members:

.. autoclass:: github4.repos.branch.ProtectionEnforceAdmins
    :members:

.. autoclass:: github4.repos.branch.ProtectionRestrictions
    :members:

.. autoclass:: github4.repos.branch.ProtectionRequiredPullRequestReviews
    :members:

.. autoclass:: github4.repos.branch.ProtectionRequiredStatusChecks
    :members:

Commits
~~~~~~~

.. autoclass:: github4.repos.commit.MiniCommit
    :members:

.. autoclass:: github4.repos.commit.ShortCommit
    :members:

.. autoclass:: github4.repos.commit.RepoCommit
    :members:

.. autoclass:: github4.repos.comparison.Comparison
    :members:


Release Objects
---------------

.. autoclass:: github4.repos.release.Asset
    :members:

.. autoclass:: github4.repos.release.Release
    :members:


Pages Objects
-------------

.. autoclass:: github4.repos.pages.PagesInfo
    :members:

.. autoclass:: github4.repos.pages.PagesBuild
    :members:


Comment Objects
---------------

More information about these classes can be found in the official documentation
about `comments <http://developer.github.com/v3/repos/comments/>`_.

.. autoclass:: github4.repos.comment.ShortComment
    :members:

.. autoclass:: github4.repos.comment.RepoComment
    :members:


Deployment and Status Objects
-----------------------------

.. autoclass:: github4.repos.deployment.Deployment
    :members:

.. autoclass:: github4.repos.deployment.DeploymentStatus
    :members:

.. autoclass:: github4.repos.status.ShortStatus
    :members:

.. autoclass:: github4.repos.status.CombinedStatus
    :members:

.. autoclass:: github4.repos.status.Status
    :members:


Contributor Statistics Objects
------------------------------

.. autoclass:: github4.repos.stats.ContributorStats
    :members:


.. ---
.. links
.. _Repositories API:
    https://developer.github.com/v3/repos/
