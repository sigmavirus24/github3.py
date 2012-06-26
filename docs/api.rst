.. _api:

API
===

.. module:: github3
.. module:: github3.api

This part of the documentation covers the API. This is intended to be a
beautifully written module which allows the user (developer) to interact with
``github3.py`` elegantly and easily.

Module Contents
---------------

To interact with the GitHub API you can either authenticate to access protected
functionality or you can interact with it anonymously. Authenticating provides
more functionality to the the user (developer).

To authenticate, you simply use :func:`github3.login`.

.. autofunction:: github3.login

With the :class:`GitHub <github3.github.GitHub>` object that is returned you have access
to more functionality. See that object's documentation for more information.

To use the API anonymously, you can create a new
:class:`GitHub <github3.github.GitHub>` object, e.g.,

::

    from github3 import GitHub

    gh = GitHub()

Or you can simply use the following functions

------

.. autofunction:: github3.create_gist

------

.. autofunction:: github3.gist

------

.. autofunction:: github3.issue

------

.. autofunction:: github3.list_events

------

.. autofunction:: github3.list_gists

------

.. autofunction:: github3.search_issues

------

.. autofunction:: github3.search_repos

------

.. autofunction:: github3.search_users

------

.. autofunction:: github3.search_email
