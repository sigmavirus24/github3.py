github3.py
==========

.. image::
    https://secure.travis-ci.org/sigmavirus24/github3.py.png?branch=mock
    :alt: Build Status
    :target: http://travis-ci.org/sigmavirus24/github3.py

github3.py is a comprehensive, actively developed and extraordinarily stable 
wrapper around the GitHub API (v3).

See HISTORY.rst for any "breaking" changes.

Installation
------------

::

    $ pip install github3.py

Dependencies
------------

- requests_  by Kenneth Reitz

.. _requests: https://github.com/kennethreitz/requests

Testing
~~~~~~~

- expecter_ by Gary Bernhardt
- mock_ by Michael Foord
- coverage_ by Ned Batchelder

.. _expecter: https://github.com/garybernhardt/expecter
.. _coverage: http://nedbatchelder.com/code/coverage/
.. _mock: http://mock.readthedocs.org/en/latest/

License
-------

Modified BSD license_

.. _license:

Examples
--------

See the docs_ for more detailed examples.

.. _docs: http://github3py.readthedocs.org/en/latest/index.html#more-examples

Create a git blob:

::

  >>> from github3 import login
  >>> g = login(username, password)
  >>> repo = g.repository('sigmavirus24', 'Todo.txt-python')
  >>> sha = repo.create_blob('Testing blob creation', 'utf-8')
  >>> sha
  u'57fad9a39b27e5eb4700f66673ce860b65b93ab8'
  >>> blob = repo.blob(sha)
  >>> blob.content
  u'VGVzdGluZyBibG9iIGNyZWF0aW9u\n'
  >>> blob.decoded
  u'Testing blob creation'
  >>> blob.encoding
  u'base64'

Create a tag on a commit:

::

  >>> from github3 import login
  >>> g = login(username, password)
  >>> repo = g.repository('sigmavirus24', 'github3.py')
  >>> tag = repo.tag('cdba84b4fede2c69cb1ee246b33f49f19475abfa')
  >>> tag
  <Tag [cdba84b4fede2c69cb1ee246b33f49f19475abfa]>
  >>> tag.object.sha
  u'24ea44d302c6394a0372dcde8fd8aed899c0034b'
  >>> tag.object.type
  u'commit'

Testing
~~~~~~~

::

    make tests

These coverage numbers are from the old-style tests and still apply to master.

::

    Name                 Stmts   Miss  Cover
    ----------------------------------------
    github3/__init__         8      0   100%
    github3/api             54      1    98%
    github3/auths           50      0   100%
    github3/decorators      27      0   100%
    github3/events          89      0   100%
    github3/gists          101      0   100%
    github3/git             93      0   100%
    github3/github         374      0   100%
    github3/issues         204      0   100%
    github3/legacy          97      0   100%
    github3/models         189      0   100%
    github3/orgs           177      0   100%
    github3/pulls          138      6    96%
    github3/repos          790     22    97%
    github3/users          160      0   100%
    ----------------------------------------
    TOTAL                 2551     29    99%

Author
------

Ian Cordasco (sigmavirus24)

Contact Options
---------------

- It is preferred that you send an email to github3.py@librelist.com
- You may also contact (via email) the author directly with 
  questions/suggestions/comments
