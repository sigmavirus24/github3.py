=================================================
github4.py: A Library for Using GitHub's REST API
=================================================

Release v\ |version|.

github4.py is wrapper for the `GitHub API`_ written in python. The design of
github4.py is centered around having a logical organization of the methods
needed to interact with the API. As an example, let's get information about a
user:

.. code-block:: python

    from github4 import login

    gh = login('staticdev', password='<password>')

    staticdev = gh.me()
    # <AuthenticatedUser [staticdev:Thiago Carvalho D'Ávila]>

    print(staticdev.name)
    # Thiago Carvalho D'Ávila
    print(staticdev.login)
    # staticdev
    print(staticdev.followers_count)
    # 4

    for f in gh.followers():
        print(str(f))

    kennethreitz = gh.user('kennethreitz')
    # <User [kennethreitz:Kenneth Reitz]>

    print(kennethreitz.name)
    print(kennethreitz.login)
    print(kennethreitz.followers_count)

    followers = [str(f) for f in gh.followers('kennethreitz')]

There are several examples of different aspects of using github4.py

.. toctree::
    :maxdepth: 2

    examples/two_factor_auth
    examples/oauth
    examples/gist
    examples/git
    examples/github
    examples/issue
    examples/iterators
    examples/logging
    examples/octocat


Installation
============

.. code-block:: console

    $ pip install github4.py


User Guide
==========

.. toctree::
    :maxdepth: 2

    narrative/index


API Reference Documentation
===========================

.. toctree::
    :maxdepth: 2

    api-reference/index

.. _Contributor Guide: CONTRIBUTING.rst

.. toctree::
   :hidden:
   :maxdepth: 1

   contributing
   Code of Conduct <codeofconduct>
   License <license>

.. links

.. _GitHub API:
    http://developer.github.com
