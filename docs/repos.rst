.. module:: github3
.. module:: github3.repos.branch
.. module:: github3.repos.comment
.. module:: github3.repos.commit
.. module:: github3.repos.comparison
.. module:: github3.repos.contents
.. module:: github3.repos.download
.. module:: github3.repos.hook
.. module:: github3.repos.repo
.. module:: github3.repos.status
.. module:: github3.repos.tag

Repository
==========

This part of the documentation covers:

- :class:`Repository <Repository>`
- :class:`Branch <Branch>`
- :class:`Contents <Contents>`
- :class:`Download <Download>`
- :class:`Hook <Hook>`
- :class:`RepoTag <RepoTag>`
- :class:`RepoComment <RepoComment>`
- :class:`RepoCommit <RepoCommit>`
- :class:`Comparison <Comparison>`
- :class:`Status <Status>`

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

.. autoclass:: Repository
    :inherited-members:

---------

.. autoclass:: Branch
    :members:

---------

.. autoclass:: Contents
    :members:

---------

.. autoclass:: Download
    :members:

---------

.. autoclass:: Hook
    :members:

---------

.. autoclass:: RepoTag
    :members:

---------

More information about this class can be found in the official documentation
about `comments <http://developer.github.com/v3/repos/comments/>`_.

.. autoclass:: RepoComment
    :inherited-members:

---------

.. autoclass:: RepoCommit
    :members:

---------

.. autoclass:: Comparison
    :members:

---------

.. autoclass:: Status
    :members:
