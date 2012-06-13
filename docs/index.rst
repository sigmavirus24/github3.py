github3.py
==========

Release v\ |version|.

github3.py is wrapper for the `GitHub API`_ written in python. The design of
github3.py is centered around having a logical organization of the methods
needed to interact with the API. Let me demonstrate this with some code
examples.

First, let's get information about a user.

::

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


.. links

.. _GitHub API: http://developer.github.com

.. toctree::
    :maxdepth: 1

    api
