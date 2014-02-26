.. module:: github3

Repository
==========

This part of the documentation covers:

- :class:`Repository <github3.repos.repo.Repository>`
- :class:`Branch <github3.repos.branch.Branch>`
- :class:`Contents <github3.repos.contents.Contents>`
- :class:`Deployment <github3.repos.deployment.Deployment>`
- :class:`DeploymentStatus <github3.repos.deployment.DeploymentStatus>`
- :class:`Hook <github3.repos.hook.Hook>`
- :class:`RepoTag <github3.repos.tag.RepoTag>`
- :class:`RepoComment <github3.repos.comment.RepoComment>`
- :class:`RepoCommit <github3.repos.commit.RepoCommit>`
- :class:`Comparison <github3.repos.comparison.Comparison>`
- :class:`Status <github3.repos.status.Status>`
- :class:`ContributorStats <github3.repos.stats.ContributorStats>`

None of these objects should be instantiated directly by the user (developer).
These are here for reference only.

**When listing repositories in any context, GitHub refuses to return a number 
of attributes, e.g., source and parent. If you require these, call the refresh 
method on the repository object to make a second call to the API and retrieve 
those attributes.**

More information for about this class can be found in the official
`documentation <http://developer.github.com/v3/repos>`_ and in various other
sections of the GitHub documentation.

Repository Objects
------------------

.. autoclass:: github3.repos.repo.Repository
    :inherited-members:

---------

.. autoclass:: github3.repos.branch.Branch
    :members:

---------

.. autoclass:: github3.repos.contents.Contents
    :members:

---------

.. autoclass:: github3.repos.deployment.Deployment
    :members:

---------

.. autoclass:: github3.repos.deployment.DeploymentStatus
    :members:

---------

.. autoclass:: github3.repos.release.Release
    :members:


---------

.. autoclass:: github3.repos.hook.Hook
    :members:

---------

.. autoclass:: github3.repos.tag.RepoTag
    :members:

---------

More information about this class can be found in the official documentation
about `comments <http://developer.github.com/v3/repos/comments/>`_.

.. autoclass:: github3.repos.comment.RepoComment
    :inherited-members:

---------

.. autoclass:: github3.repos.commit.RepoCommit
    :members:

---------

.. autoclass:: github3.repos.comparison.Comparison
    :members:

---------

.. autoclass:: github3.repos.status.Status
    :members:

---------

.. autoclass:: github3.repos.stats.ContributorStats
    :members:
