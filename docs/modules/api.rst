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

.. autofunction:: github3.authorize

------

.. autofunction:: github3.create_gist

------

.. autofunction:: github3.gist

------

.. autofunction:: github3.gitignore_template

------

.. autofunction:: github3.gitignore_templates

------

.. autofunction:: github3.issue

------

.. autofunction:: github3.iter_all_repos

------

.. autofunction:: github3.iter_all_users

------

.. autofunction:: github3.iter_events

------

.. autofunction:: github3.iter_followers

------

.. autofunction:: github3.iter_following

------

.. autofunction:: github3.iter_gists

------

.. autofunction:: github3.iter_orgs

------

.. autofunction:: github3.iter_user_repos

------

.. autofunction:: github3.iter_repo_issues

------

.. autofunction:: github3.iter_starred

------

.. autofunction:: github3.iter_subscriptions

------

.. autofunction:: github3.markdown

------

.. autofunction:: github3.octocat

------

.. autofunction:: github3.organization

------

.. autofunction:: github3.pull_request

------

.. autofunction:: github3.ratelimit_remaining

------

.. autofunction:: github3.repository

------

.. autofunction:: github3.search_code

------

.. autofunction:: github3.search_issues

------

.. autofunction:: github3.search_repositories

------

.. autofunction:: github3.search_users


------

.. autofunction:: github3.user

------

.. autofunction:: github3.zen

------

Enterprise Use
--------------

If you're using github3.py to interact with an enterprise installation of 
GitHub, you must use the
:class:`GitHubEnterprise <github3.github.GitHubEnterprise>` object. Upon 
initialization, the only parameter you must supply is the URL of your 
enterprise installation, e.g.

::

    from github import GitHubEnterprise

    g = GitHubEnterprise('https://github.examplesintl.com')
    stats = g.admin_stats('all')
    assert 'issues' in stats, ('Key issues is not included in the admin'
                               'statistics')
