============================
 Custom Iterator Structures
============================

Many of the methods in github4.py that return iterators of another object are
actually returning one of the iterators below. These iterators effectively
allow users to ignore GitHub's API pagination of large sets of data. In all
senses, they behave like a normal Python iterator. Their difference is that
they have extra logic around making API requests and coercing the JSON into
predefined objects.

.. autoclass:: github4.structs.GitHubIterator
    :inherited-members:

.. autoclass:: github4.structs.SearchIterator
    :inherited-members:
