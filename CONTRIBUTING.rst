Guidelines for Contributing to github3.py
=========================================

0. Read the README_

1. Regardless of the magnitude your pull request (a couple lines to a couple 
   hundred lines), please add your name to the AUTHORS.rst file under the 
   heading Contributors.

2. If you're fixing a bug, please write a regression test. All the tests are 
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

3. If you're adding a new section of the API that does not already exist, 
   please also add tests to the test suite.

4. If you're adding additional functionality beyond what the API covers, 
   please open an issue reqeust first and of course add tests to cover the 
   functionality in the event it is accepted.

   Also, please be certain to add docstrings_ to these functions. Follow the 
   example of other docstrings.

5. In case you haven't caught on, for anything you add, write tests.

6. Be cordial_.

7. Rebase your fork/branch if needed and possible before submitting a pull 
   request. This makes my life easier. If you honestly have no idea what I'm 
   talking about, don't worry, I'll take care of it.

8. Please follow pep-0008_. Feel free to also use flake8_ to help.

.. links
.. _README: ./README.rst
.. _cordial: http://kennethreitz.com/be-cordial-or-be-on-your-way.html
.. _pep-0008: http://www.python.org/dev/peps/pep-0008/
.. _docstrings: http://www.python.org/dev/peps/pep-0257/
.. _flake8: http://pypi.python.org/pypi/flake8
