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


More Examples
~~~~~~~~~~~~~

.. toctree::
    :maxdepth: 2

    examples/gist
    examples/github
    examples/issue


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
    legacy
    org
    pulls
    repo
    user

Internals
~~~~~~~~~

For objects you're not likely to see in practice. This is useful if you ever
feel the need to contribute to the project.

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

- Search

- Markdown

Contributing
------------

I'm maintaining two public copies of the project. The first can be found on 
GitHub_ and the second on BitBucket_. I would prefer pull requests to take 
place on GitHub, but feel free to do them via BitBucket. Please make sure to 
add yourself to the list of contributors in AUTHORS.rst, especially if you're 
going to be working on the list below.

.. links
.. _GitHub: https://github.com/sigmavirus24/github3.py
.. _BitBucket: https://bitbucket.org/icordasc/github3.py/src

Contributor Friendly Work
~~~~~~~~~~~~~~~~~~~~~~~~~

In order of importance:

:func:`create_download <github3.repo.Repository.create_download>`

    If you're familiar with Amazon's S3 web services and have the patience to 
    debug this function, I would greatly appreciate it.

Unittests

    I really should have written these as I wrote the code. I didn't, so they 
    need to be written now. If you want to write some, I would sinerely 
    appreciate it.

Documentation

    I know I'm not the best at writing documentation so if you want to clarify 
    or correct something, please do so.

Examples

    Have a clever example that takes advantage of github3.py? Feel free to 
    share it.

Contact
-------

- Twitter: @sigmavirus24_
- Private email: graffatcolmingov [at] gmail
- Mailing list: github3.py [at] librelist.com

.. _sigmavirus24: https://twitter.com/sigmavirus24
