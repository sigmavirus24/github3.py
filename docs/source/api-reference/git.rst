=================
 Git API Classes
=================

This part of the documentation covers the module associated with the
`Git Data`_ section of the GitHub API.

Like much of the GitHub API, many objects have different representations.


Blob Object(s)
==============

.. autoclass:: github3.git.Blob


Commit Object(s)
================

.. autoclass:: github3.git.Commit

.. autoclass:: github3.git.ShortCommit


Tree Object(s)
==============

.. autoclass:: github3.git.CommitTree

.. autoclass:: github3.git.Hash

.. autoclass:: github3.git.Tree


Git Object, Reference, and Tag Object(s)
========================================

Yes, we know, ``GitObject`` is a funky name.

.. autoclass:: github3.git.GitObject

.. autoclass:: github3.git.Reference

.. autoclass:: github3.git.Tag


.. links
.. _Git Data:
    https://developer.github.com/v3/git/
