.. module:: github3

Repository
==========

This part of the documentation covers:

- :class:`Repository <github3.repos.repo.Repository>`
- :class:`Asset <github3.repos.release.Asset>`
- :class:`Branch <github3.repos.branch.Branch>`
- :class:`Contents <github3.repos.contents.Contents>`
- :class:`Deployment <github3.repos.deployment.Deployment>`
- :class:`DeploymentStatus <github3.repos.deployment.DeploymentStatus>`
- :class:`Hook <github3.repos.hook.Hook>`
- :class:`PagesInfo <github3.repos.pages.PagesInfo>`
- :class:`PagesBuild <github3.repos.pages.PagesBuild>`
- :class:`Release <github3.repos.release.Release>`
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

.. module:: github3.repos.repo

.. autoclass:: github3.repos.repo.Repository
    :inherited-members:

---------

.. module:: github3.repos.branch

.. autoclass:: github3.repos.branch.Branch
    :members:

---------

.. module:: github3.repos.contents

.. autoclass:: github3.repos.contents.Contents
    :members:

---------

.. module:: github3.repos.deployment

.. autoclass:: github3.repos.deployment.Deployment
    :members:

---------

.. autoclass:: github3.repos.deployment.DeploymentStatus
    :members:

---------

.. module:: github3.repos.release

.. autoclass:: github3.repos.release.Release
    :members:

---------

.. autoclass:: github3.repos.release.Asset
    :members:

---------

.. module:: github3.repos.hook

.. autoclass:: github3.repos.hook.Hook
    :members:

---------

.. module:: github3.repos.pages

.. autoclass:: github3.repos.pages.PagesInfo
    :members:

---------

.. autoclass:: github3.repos.pages.PagesBuild
    :members:

---------

.. module:: github3.repos.tag

.. autoclass:: github3.repos.tag.RepoTag
    :members:

---------

.. module:: github3.repos.comment

More information about this class can be found in the official documentation
about `comments <http://developer.github.com/v3/repos/comments/>`_.

.. autoclass:: github3.repos.comment.RepoComment
    :inherited-members:

---------

.. module:: github3.repos.commit

.. autoclass:: github3.repos.commit.RepoCommit
    :members:

---------

.. module:: github3.repos.comparison

.. autoclass:: github3.repos.comparison.Comparison
    :members:

---------

.. module:: github3.repos.status

.. autoclass:: github3.repos.status.Status
    :members:

---------

.. module:: github3.repos.stats

.. autoclass:: github3.repos.stats.ContributorStats
    :members:
