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

    for f in gh.iter_followers():
        print(str(f))

    kennethreitz = gh.user('kennethreitz')
    # <User [kennethreitz:Kenneth Reitz]>

    print(kennethreitz.name)
    print(kennethreitz.login)
    print(kennethreitz.followers)

    followers = [str(f) for f in gh.iter_followers('kennethreitz')]

More Examples
~~~~~~~~~~~~~

.. toctree::
    :maxdepth: 2

    examples/oauth
    examples/gist
    examples/git
    examples/github
    examples/issue


.. links

.. _GitHub API: http://developer.github.com


Modules
-------

.. toctree::
    :maxdepth: 1

    api
    auths
    events
    gists
    git
    github
    issues
    legacy
    models
    orgs
    pulls
    repos
    users

Internals
~~~~~~~~~

For objects you're not likely to see in practice. This is useful if you ever
feel the need to contribute to the project.

.. toctree::
    :maxdepth: 1

    models
    decorators


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

Documentation

    I know I'm not the best at writing documentation so if you want to clarify 
    or correct something, please do so.

Examples

    Have a clever example that takes advantage of github3.py? Feel free to 
    share it.

Running the Unittests
~~~~~~~~~~~~~~~~~~~~~

::

    mkdir -p /path/to/virtualenv/github3.py
    cd /path/to/virtualenv/github3.py
    virtualenv .
    cd /path/to/github3.py_repo/requirements.txt
    pip install -r requirements.txt
    # Or you could run make test-deps
    make tests


Contact
-------

- Twitter: @\ sigmavirus24_
- Private email: graffatcolmingov [at] gmail
- Mailing list: github3.py [at] librelist.com

.. _sigmavirus24: https://twitter.com/sigmavirus24

.. include:: ../HISTORY.rst
