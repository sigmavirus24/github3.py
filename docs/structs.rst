.. module:: github3
.. module:: github3.structs

Structures
==========

Developed for github3.py
------------------------

As of right now, there exists only one class in this section, and it is of 
only limited importance to users of github3.py. The :class:`GitHubIterator` 
class is used to return the results of calls to almost all of the calls to 
``iter_`` methods on objects. When conditional refreshing was added to 
objects, there was a noticable gap in having conditional calls to those 
``iter_`` methods.  GitHub provides the proper headers on those calls, but 
there was no easy way to add that to what github3.py returned so it could be 
used properly. This was the best compromise - an object the behaves like an 
iterator regardless but can also be ``refresh``\ ed to get results since the 
last request conditionally.

Objects
-------

.. autoclass:: GitHubIterator
    :inherited-members:


.. autoclass:: SearchIterator
    :inherited-members:
