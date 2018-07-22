========================
 Repository API Objects
========================

This section of the documentation covers the representations of various
objects related to the `Repositories API`_.


Repository Objects
------------------

.. autoclass:: github3.repos.repo.Repository
    :inherited-members:

.. autoclass:: github3.repos.repo.ShortRepository
    :inherited-members:

.. autoclass:: github3.repos.repo.StarredRepository
    :inherited-members:

.. autoclass:: github3.repos.contents.Contents
    :members:

.. autoclass:: github3.repos.hook.Hook
    :members:

.. autoclass:: github3.repos.issue_import.ImportedIssue
    :members:


Git-related Objects
-------------------

.. autoclass:: github3.repos.tag.RepoTag
    :members:

Branches
~~~~~~~~

.. autoclass:: github3.repos.branch.Branch
    :members:

.. autoclass:: github3.repos.branch.ShortBranch
    :members:

.. autoclass:: github3.repos.branch.BranchProtection
    :members:

.. autoclass:: github3.repos.branch.ProtectionEnforceAdmins
    :members:

.. autoclass:: github3.repos.branch.ProtectionRestrictions
    :members:

.. autoclass:: github3.repos.branch.ProtectionRequiredPullRequestReviews
    :members:

.. autoclass:: github3.repos.branch.ProtectionRequiredStatusChecks
    :members:

Commits
~~~~~~~

.. autoclass:: github3.repos.commit.MiniCommit
    :members:

.. autoclass:: github3.repos.commit.ShortCommit
    :members:

.. autoclass:: github3.repos.commit.RepoCommit
    :members:

.. autoclass:: github3.repos.comparison.Comparison
    :members:


Release Objects
---------------

.. autoclass:: github3.repos.release.Asset
    :members:

.. autoclass:: github3.repos.release.Release
    :members:


Pages Objects
-------------

.. autoclass:: github3.repos.pages.PagesInfo
    :members:

.. autoclass:: github3.repos.pages.PagesBuild
    :members:


Comment Objects
---------------

More information about these classes can be found in the official documentation
about `comments <http://developer.github.com/v3/repos/comments/>`_.

.. autoclass:: github3.repos.comment.ShortComment
    :members:

.. autoclass:: github3.repos.comment.RepoComment
    :members:


Deployment and Status Objects
-----------------------------

.. autoclass:: github3.repos.deployment.Deployment
    :members:

.. autoclass:: github3.repos.deployment.DeploymentStatus
    :members:

.. autoclass:: github3.repos.status.ShortStatus
    :members:

.. autoclass:: github3.repos.status.CombinedStatus
    :members:

.. autoclass:: github3.repos.status.Status
    :members:


Contributor Statistics Objects
------------------------------

.. autoclass:: github3.repos.stats.ContributorStats
    :members:


.. ---
.. links
.. _Repositories API:
    https://developer.github.com/v3/repos/
