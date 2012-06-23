github3.py
==========

Release v\ |version|.

github3.py is wrapper for the `GitHub API`_ written in python. The design of
github3.py is centered around having a logical organization of the methods
needed to interact with the API. Let me demonstrate this with a code example.

Example
-------

Let's get information about a user::

    from github3 import login

    gh = login('sigmavirus24', password='<password>')

    sigmavirus24 = gh.user()
    # <User [sigmavirus24:Ian Cordasco]>

    print(sigmavirus24.name)
    # Ian Cordasco
    print(sigmavirus24.login)
    # sigmavirus24
    print(sigmavirus24.followers)
    # 4

    gh.list_followers()

    kennethreitz = gh.user('kennethreitz')
    # <User [kennethreitz:Kenneth Reitz]>

    print(kennethreitz.name)
    print(kennethreitz.login)
    print(kennethreitz.followers)

    gh.list_followers('kennethreitz')


Further Examples
~~~~~~~~~~~~~~~~

.. toctree::
    :maxdepth: 2

    examples/gist
    examples/github


.. links

.. _GitHub API: http://developer.github.com


Modules
-------

.. toctree::
    :maxdepth: 1

    api
    event
    gist
    git
    github
    issue
    org
    pulls
    repo

Internals
~~~~~~~~~

For objects you're not likely to see in practice.

.. toctree::
    :maxdepth: 1

    models


Installation
------------

.. code-block:: sh

    $ pip install github3.py
    # OR:
    $ git clone git://github.com/sigmavirus24/github3.py.git github3.py
    $ cd github3.py
    $ python setup.py install


Dependencies
~~~~~~~~~~~~

- requests_ by Kenneth Reitz

.. _requests: https://github.com/kennethreitz/requests


API Coverage
------------

- Gists

  - Comments

- Git Data

  - Blobs
  - Commits
  - References
  - Tags
  - Trees

- Issues

  - Comments
  - Events
  - Labels
  - Milestones

- Orgs

  - Members
  - Teams

- Pull Requests

  - Review Comments

- Repos

  - Collaborators
  - Comments
  - Commits
  - Contents
  - Downloads
  - Forks
  - Keys
  - Watching
  - Hooks

- Users

  - Emails
  - Followers
  - Keys

- Events

  - Types
