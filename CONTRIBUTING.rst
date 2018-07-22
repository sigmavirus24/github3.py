Guidelines for Contributing to github3.py
=========================================

#. Read the README_

#. Please do **not** use the issue tracker for questions.

#. Please use GitHub's search feature to look for already reported issues 
   before reporting your own.

#. Regardless of the magnitude your pull request (a couple lines to a couple 
   hundred lines), please add your name to the AUTHORS.rst_ file under the 
   heading Contributors.

#. There is a label for issues that should be minor and should be a good way
   to become acquainted with the project. The easy_ label is the over-arching 
   way to determine which issues you can dig into without a great deal of 
   prior knowledge. Most of these issues have a `Pair with Ian`_ label which 
   means that if you would like, I (@sigmavirus24) will happily pair program 
   with you to solve the issue.

#. If you're fixing a bug, please write a regression test. All the tests are 
   structured like so::

    tests/
    - test_<module_name>.py
        + Test<ClassName>
          - def test_function_or_attribute

   Please do not add your regression test to an existing test, but create a 
   new one. You can use the form ``test_issue_<number>``. In a docstring add 
   the link and a short description of the regression issue. For example, if 
   you found a bug in the class ``Issue``, write your test in the file 
   ``test_issues.py`` in the class ``TestIssue``. You can place the new test 
   in any order, e.g., below all the existing tests, near a related one, &c.

#. If you're adding a new section of the API that does not already exist, 
   please also add tests to the test suite.

#. If you're adding additional functionality beyond what the API covers, 
   please open an issue request first and of course add tests to cover the 
   functionality in the event it is accepted.

   Also, please be certain to add docstrings_ to these functions. Follow the 
   example of other docstrings.

#. In case you haven't caught on, for anything you add, write tests.

#. Be cordial_. Seriously, anyone who isn't cordial will be sent packing, 
   regardless of the value of their contributions. I will not tolerate some 
   contributors creating a hostile environment for others.

#. Rebase your fork/branch if needed and possible before submitting a pull 
   request. This makes my life easier. If you honestly have no idea what I'm 
   talking about, don't worry, I'll take care of it.

#. Please follow pep-0008_. Feel free to also use flake8_ to help.

.. links
.. _README: ./README.rst
.. _easy: https://github.com/sigmavirus24/github3.py/issues?labels=Easy&page=1&state=open
.. _Pair with Ian: https://github.com/sigmavirus24/github3.py/issues?labels=Pair+with+Ian&page=1&state=open
.. _AUTHORS.rst: ./AUTHORS.rst
.. _cordial: http://www.kennethreitz.org/essays/be-cordial-or-be-on-your-way
.. _pep-0008: http://www.python.org/dev/peps/pep-0008/
.. _docstrings: http://www.python.org/dev/peps/pep-0257/
.. _flake8: http://pypi.python.org/pypi/flake8
