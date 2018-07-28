===================================================
 github3.py: A Library for Using GitHub's REST API
===================================================

Release v\ |version|.

github3.py is wrapper for the `GitHub API`_ written in python. The design of
github3.py is centered around having a logical organization of the methods
needed to interact with the API. As an example, let's get information about a
user:

.. code-block:: python

    from github3 import login

    gh = login('sigmavirus24', password='<password>')

    sigmavirus24 = gh.me()
    # <AuthenticatedUser [sigmavirus24:Ian Stapleton Cordasco]>

    print(sigmavirus24.name)
    # Ian Stapleton Cordasco
    print(sigmavirus24.login)
    # sigmavirus24
    print(sigmavirus24.followers_count)
    # 4

    for f in gh.followers():
        print(str(f))

    kennethreitz = gh.user('kennethreitz')
    # <User [kennethreitz:Kenneth Reitz]>

    print(kennethreitz.name)
    print(kennethreitz.login)
    print(kennethreitz.followers_count)

    followers = [str(f) for f in gh.followers('kennethreitz')]

There are several examples of different aspects of using github3.py

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

    $ pip install github3.py


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


Version History
===============

.. toctree::
    :maxdepth: 2

    release-notes/index


Contributing
============

All development happens on GitHub_. Please remember to add yourself to the
list of contributors in AUTHORS.rst, especially if you're going to be
working on the list below.

Contributor Friendly Work
-------------------------

In order of importance:

Documentation

    I know I'm not the best at writing documentation so if you want to clarify
    or correct something, please do so.

Examples

    Have a clever example that takes advantage of github3.py? Feel free to
    share it.

Otherwise, feel free to example the list of issues where we would like help_
and feel free to take one.

Running the Unittests
---------------------

The tests are generally run using tox. Tox can be installed like so

.. code-block:: console

    pip install tox

We test against PyPy and the following versions of Python:

- 2.7

- 3.4

- 3.5

- 3.6

If you simply run ``tox`` it will run tests against all of these versions of
python and run ``flake8`` against the codebase as well. If you want to run
against one specific version, you can do

.. code-block:: console

    tox -e py36

And if you want to run tests against a specific file, you can do

.. code-block:: console

    tox -e py36 -- tests/unit/test_github.py

To run the tests, ``tox`` uses ``py.test`` so you can pass any options or
parameters to ``py.test`` after specifying ``--``. For example, you can get
more verbose output by doing

.. code-block:: console

    tox -e py36 -- -vv

.. toctree::

    contributing/testing


Contact
=======

- Twitter: `@sigmavirus24`_
- Private email: graffatcolmingov [at] gmail

.. _@sigmavirus24: https://twitter.com/sigmavirus24


.. links

.. _GitHub API:
    http://developer.github.com
.. _GitHub:
    https://github.com/sigmavirus24/github3.py
.. _help:
    https://github.com/sigmavirus24/github3.py/labels/help%20wanted
