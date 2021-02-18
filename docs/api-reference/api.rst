.. _api:

==========================
 Anonymous Functional API
==========================

.. module:: github4
.. module:: github4.api

This part of the documentation covers the API. This is intended to be a
beautifully written module which allows the user (developer) to interact with
``github4.py`` elegantly and easily.

Module Contents
===============

To interact with the GitHub API you can either authenticate to access protected
functionality or you can interact with it anonymously. Authenticating provides
more functionality to the user (developer).

To authenticate, you may use :func:`github4.login`.

.. autofunction:: github4.login

With the :class:`~github4.github.GitHub` object that is returned you have
access to more functionality. See that object's documentation for more
information.

To use the API anonymously, you can also create a new
:class:`~github4.github.GitHub` object, e.g.,

.. code-block:: python

    from github4 import GitHub

    gh = GitHub()

Enterprise Use
==============

If you're using github4.py to interact with an enterprise installation of
GitHub, you **must** use the :class:`~github4.github.GitHubEnterprise` object.
Upon initialization, the only parameter you must supply is the URL of your
enterprise installation, e.g.

.. code-block:: python

    from github4 import GitHubEnterprise

    g = GitHubEnterprise('https://github.examplesintl.com')
    stats = g.admin_stats('all')
    assert 'issues' in stats, ('Key issues is not included in the admin'
                               'statistics')
