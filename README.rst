github3.py
==========

Eventually this will be a python module to access the GitHub v3 API.

Easy Cloning
------------

Assuming you have git 1.7.x (although I'm not entirely certain what version
it was introduced in) you can perform ``git clone --recursive
git://github.com/sigmavirus24/github3.py.git github3.py`` to clone this 
and the submodule at the same time. Otherwise you have to do:

::

    $ git clone git://github.com/sigmavirus24/github3.py.git
    $ cd github3.py
    $ git submodule init
    $ git submodule update

Dependencies
------------

- requests_  by Kenneth Reitz
  
.. _requests: https://github.com/kennethreitz/requests

License
-------

Modified BSD license_

.. _license:

Examples
--------

::

  >>> from github3 import login
  >>> gh = login(username, password)
  >>> gists = gh.gists()
  >>> files = {'spam.txt' : {'content': 'What... is the air-speed velocity of an
  unladen swallow?'}}
  >>> gh.create_gist('Answer this to cross the bridge', files, public=False)
  <Gist [gist-id]>

Author
------

Sigmavirus24
