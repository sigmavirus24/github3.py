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

You can run either ``pip install -r requirements.txt`` to install the 
following before testing or simply ``make test-deps``. It is suggested you do 
this in a virtual enviroment. These need to be installed for the tests to run.

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

See the docs_ for more examples.

.. _docs: http://github3py.readthedocs.org/en/latest/index.html#more-examples

Testing
~~~~~~~

Install the dependencies from requirements.txt e.g.:

::

    pip install -r requirements.txt
    # or make test-deps

::

    make tests

Author
------

Ian Cordasco (sigmavirus24)

Contact Options
---------------

- It is preferred that you send an email to github3.py@librelist.com
- You may also contact (via email) the author directly with 
  questions/suggestions/comments
