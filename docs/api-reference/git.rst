=================
 Git API Classes
=================

This part of the documentation covers the module associated with the
`Git Data`_ section of the GitHub API.

Like much of the GitHub API, many objects have different representations.


Blob Object(s)
==============

.. autoclass:: github4.git.Blob


Commit Object(s)
================

.. autoclass:: github4.git.Commit

.. autoclass:: github4.git.ShortCommit


Tree Object(s)
==============

.. autoclass:: github4.git.CommitTree

.. autoclass:: github4.git.Hash

.. autoclass:: github4.git.Tree


Git Object, Reference, and Tag Object(s)
========================================

Yes, we know, ``GitObject`` is a funky name.

.. autoclass:: github4.git.GitObject

.. autoclass:: github4.git.Reference

.. autoclass:: github4.git.Tag


.. links
.. _Git Data:
    https://developer.github.com/v3/git/
