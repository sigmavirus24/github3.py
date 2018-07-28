.. _api:

==========================
 Anonymous Functional API
==========================

.. module:: github3
.. module:: github3.api

This part of the documentation covers the API. This is intended to be a
beautifully written module which allows the user (developer) to interact with
``github3.py`` elegantly and easily.

Module Contents
===============

To interact with the GitHub API you can either authenticate to access protected
functionality or you can interact with it anonymously. Authenticating provides
more functionality to the user (developer).

To authenticate, you may use :func:`github3.login`.

.. autofunction:: github3.login

With the :class:`~github3.github.GitHub` object that is returned you have
access to more functionality. See that object's documentation for more
information.

To use the API anonymously, you can also create a new
:class:`~github3.github.GitHub` object, e.g.,

.. code-block:: python

    from github3 import GitHub

    gh = GitHub()

Or you can use the following functions:

Anonymous Functions
-------------------

.. autofunction:: github3.authorize

Deprecated Functions
~~~~~~~~~~~~~~~~~~~~

.. warning::

    Due to GitHub's anonymous rate limits, it's strongly advised that you don't
    use these functions.

.. autofunction:: github3.create_gist

.. autofunction:: github3.gist

.. autofunction:: github3.gitignore_template

.. autofunction:: github3.gitignore_templates

.. autofunction:: github3.issue

.. autofunction:: github3.issues_on

.. autofunction:: github3.all_repositories

.. autofunction:: github3.all_users

.. autofunction:: github3.all_events

.. autofunction:: github3.followers_of

.. autofunction:: github3.followed_by

.. autofunction:: github3.public_gists

.. autofunction:: github3.gists_by

.. autofunction:: github3.organizations_with

.. autofunction:: github3.repositories_by

.. autofunction:: github3.starred_by

.. autofunction:: github3.subscriptions_for

.. autofunction:: github3.markdown

.. autofunction:: github3.octocat

.. autofunction:: github3.organization

.. autofunction:: github3.pull_request

.. autofunction:: github3.rate_limit

.. autofunction:: github3.repository

.. autofunction:: github3.search_code

.. autofunction:: github3.search_issues

.. autofunction:: github3.search_repositories

.. autofunction:: github3.search_users

.. autofunction:: github3.user

.. autofunction:: github3.zen

Enterprise Use
==============

If you're using github3.py to interact with an enterprise installation of
GitHub, you **must** use the :class:`~github3.github.GitHubEnterprise` object.
Upon initialization, the only parameter you must supply is the URL of your
enterprise installation, e.g.

.. code-block:: python

    from github3 import GitHubEnterprise

    g = GitHubEnterprise('https://github.examplesintl.com')
    stats = g.admin_stats('all')
    assert 'issues' in stats, ('Key issues is not included in the admin'
                               'statistics')
