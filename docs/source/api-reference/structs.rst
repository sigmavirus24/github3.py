============================
 Custom Iterator Structures
============================

Many of the methods in github3.py that return iterators of another object are
actually returning one of the iterators below. These iterators effectively
allow users to ignore GitHub's API pagination of large sets of data. In all
senses, they behave like a normal Python iterator. Their difference is that
they have extra logic around making API requests and coercing the JSON into
predefined objects.

.. autoclass:: github3.structs.GitHubIterator
    :inherited-members:

.. autoclass:: github3.structs.SearchIterator
    :inherited-members:
