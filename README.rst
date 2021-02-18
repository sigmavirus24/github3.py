github4.py
==========

github4.py an actively developed wrapper around the GitHub API that forks github3.py_.

Note: This library currently works with Python 3.7+ or pypy3. For older versions, please use github3.py_ version 1.3.0.

Installation
------------

You can install *github4.py* via pip_ from PyPI_:

.. code:: console

   $ pip install github4.py

Dependencies
------------

- requests_
- uritemplate_

.. _requests: https://github.com/kennethreitz/requests
.. _uritemplate: https://github.com/sigmavirus24/uritemplate

Contributing
------------

Please read the `CONTRIBUTING`_ document.

.. _CONTRIBUTING: https://github.com/staticdev/github4.py/blob/master/CONTRIBUTING.rst

Testing
~~~~~~~

You can run either ``pip install -r dev-requirements.txt`` to install the
following before testing or simply ``make test-deps``. It is suggested you do
this in a virtual environment. These need to be installed for the tests to run.

- betamax_
- coverage_ by Ned Batchelder

.. _betamax: https://github.com/sigmavirus24/betamax
.. _coverage: http://nedbatchelder.com/code/coverage/

Build status
~~~~~~~~~~~~

You can find `master` build statuses for different environments.

- Github_
- appveyor_

.. _Github: https://github.com/staticdev/github4.py/actions
.. _appveyor: https://ci.appveyor.com/project/sigmavirus24/github3-py/branch/master

Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.

License
-------

Distributed under the terms of the MIT_ license,
*github4.py* is free and open source software.

Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.

Examples
--------

See the docs_ for more examples.

.. _docs: https://github3.readthedocs.io/en/latest/index.html#more-examples

Credits
-------

Original author of github3.py_ is Ian Stapleton Cordasco (sigmavirus24_).

.. _sigmavirus24: https://github.com/sigmavirus24
.. _github3.py: http://stackoverflow.com/questions/tagged/github3.py
.. _MIT: http://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _file an issue: https://github.com/staticdev/github4.py/issues
.. _pip: https://pip.pypa.io/
.. _Contributor Guide: CONTRIBUTING.rst
