Writing Tests for github3.py
============================

Writing tests for github3.py is a non-trivial task and takes some 
understanding of the expecter_ module and mock_ modules.

expecter
--------

I chose to use the expecter_ module in the tests for github3.py because I feel 
that writing tests with it read far more naturally. Take for instance the 
following:

.. code-block:: python

    x = 1

    def foo(x):
        return [x + 1]

    self.assertEquals(foo(x), [x + 1])

You have the variable ``x``, the function ``foo`` and the inherited 
``assertEquals`` method from ``unittest.TestCase``. My first issue with this 
is that the unittest module, although technically grandfathered in, uses 
camel-casing for its methods. To me, this is ugly and annoying to type. I've 
found myself typing ``self.assertequals`` more often than not. Now consider 
this:

.. code-block:: python

    x = 1

    def foo(x):
        return [x + 1]

    expect(foo(x)) == [x + 1]

This tests the exact same thing but this reads differently. Instead of "assert 
that ``foo(x)`` and ``[x + 1]`` are equal", you're saying "expect ``foo(x)`` 
and ``[x + 1]`` to be equal". It's the same thing, but the latter reads better 
than the former to me.

The standard ``expecter`` module has fewer methods than what we use in 
github3.py but that's because I've subclassed the ``expect`` class and renamed 
it to look the same in github3.py. So the extra functionality are the 
following methods:

- ``is_not_None`` which expects the object passed in to be anything but 
  ``None``. Example usage::

      expect(a).is_not_None()

- ``is_None`` which expects the opposite of ``is_not_None``. Example usage::

      expect(None).is_None()

- ``is_True`` which expects the object passed in to be True. Example usage::

      expect(True).is_True()

- ``is_False`` which expects the object passed in to be False. Example usage::

      expect(False).is_False()

- ``is_in(iterable)`` which expects the object passed in be in ``iterable``.  
  Example usage::

      expect('foo').is_in(['foo', 'bar', 'bogus'])

- ``githuberror`` which is used as a context manager to show that we're 
  expecting something to raise a ``GitHubError``. Example usage::

      with expect.githuberror():
          github3.authorize()

Why implement these custom methods?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using ``expecter.expect``, you receive an instance of a class instead of 
the actual object, so where you would like the following to work, it does not:

.. code-block:: python

    expect(a) is not None

The reality, however, is that test is tautologically true. Every instance of 
``expecter.expect`` is not ``None``. In other cases, tools like ``pep8`` and 
``flake8`` will complain if you do:

.. code-block:: python

    expect(a) == True

And they rightfully complain. So these methods just make life easier. If they 
cause significant enough confusion, then I'll consider rewriting the test 
suite in something better.

mock
----

The mock library written by Michael Foord is a fantastic tool and is entirely 
necessary to testing github3.py. Last year, GitHub changed their ratelimit 
(for anonymous requests) from 5000 per hour to 60 per hour. This meant that 
all of a sudden, github3.py's tests failed and failed miserably when trying to 
test directly against the API. The best solution was to collect all of the 
possible JSON responses and store then locally. You can find them in 
``tests/json/``. We then had to construct our own fake ``requests.Response`` 
objects and mock the ``request`` method on ``requests.Session`` objects. To 
help do this, I wrote some methods that are present on the ``BaseCase`` class:

- ``response`` takes the name of the file in ``tests/json``, the 
  ``status_code``, the "default" encoding for the data, optional headers and a 
  paramtere ``_iter`` which determines if the results should be iterable or 
  not. This then constructs a ``requests.Response`` object and sets it as the 
  return value of the mocked ``requests.Session#request`` method.

- ``get``, ``put``, ``patch``, ``post``, ``delete`` all modify a tuple that 
  looks like: ``(METHOD, url)`` where ``METHOD`` is either ``GET``, ``PUT``, 
  &c. and the ``url`` is passed to the method.

- ``mock_assertions`` has a set of assertions it makes about **every** request 
  we deal with and which are true of every request to the API. After making 
  these assertions, it resets the mock in case it needs to be used again 
  during the same test.

- ``not_called`` asserts that at no point was the mock used up until this 
  point.

The ``setUp`` and ``tearDown`` methods take care of instantiating the mock 
object that we use in this case. The code for those methods are taken directly 
from mocks documentation.

Walking through a couple real tests
-----------------------------------

Simple
~~~~~~

From ``tests/test_gists.py``:

.. code-block:: python

    def test_unstar(self):
        self.response('', 204)
        self.delete(self.api)
        self.conf = {}

        with expect.githuberror():
            self.gist.unstar()

        self.not_called()
        self.login()
        expect(self.gist.unstar()).is_True()
        self.mock_assertions()

First notice that this, like every other test, is prefaced with ``test_`` and 
then followed by the name of the method it is testing, in this case, 
``unstar``.

The first thing we then do is call ``self.response('', 204)`` which means 
we're going to be mocking a response with No Content and a status code of 204.  
Then we cal ``self.delete(self.api)``. ``self.api`` is an attribute I've set 
on this class which has the URL that will be used to communicate with the 
GitHub API 90% of the time. (Other times it may be modified.) ``self.delete`` 
simply sets ``self.args = ('DELETE', self.api)``. Then we use one of our 
custom expect methods. Right now, the ``Gist`` object stored in ``self.gist`` 
thinks the user is anonymous so calling ``unstar`` on it should raise a 
``GitHubError``. If it didn't, expect would raise an ``AssertionError`` 
exception and the test would fail. If that does not happen, then we just check 
(because we're paranoid) that the mock was not called with 
``self.not_called``. Next we login, and assert that calling ``unstar`` results 
in ``True``. Finally, we make sure those core assertions about the mock held.

Moderate
~~~~~~~~

From ``tests/test_gists.py``:

.. code-block:: python

    def test_create_comment(self):
        self.response('gist_comment', 201)
        self.post(self.api + '/comments')
        self.conf = {'data': {'body': 'bar'}}

        with expect.githuberror():
            self.gist.create_comment(None)

        self.login()

        expect(self.gist.create_comment(None)).is_None()
        expect(self.gist.create_comment('')).is_None()
        self.not_called()
        expect(self.gist.create_comment('bar')).isinstance(
            gists.comment.GistComment)
        self.mock_assertions()

Now we're setting an attribute called ``conf`` with ``{'data': {'body': 
'bar'}}``. We use this to assert that the data we're sending to GitHub is 
actually sent.

You'll now see that there are two calls to ``create_comment`` where we expect 
to receive ``None`` because github3.py refused to act on bad data. We then 
make sure that nothing was called and create a comment with the text ``'bar'`` 
and expect it to return an instance of ``GistComment``. Notice how the 
**body** of the new comment is **bar**.

Difficult
~~~~~~~~~

From ``tests/test_repos.py``:

.. code-block:: python

    def test_archive(self):
        headers = {'content-disposition': 'filename=foo'}
        self.response('archive', 200, **headers)  #**
        self.get(self.api + 'tarball/master')
        self.conf.update({'stream': True})

        expect(self.repo.archive(None)).is_False()

        expect(os.path.isfile('foo')).is_False()
        expect(self.repo.archive('tarball')).is_True()
        expect(os.path.isfile('foo')).is_True()
        os.unlink('foo')
        self.mock_assertions()

        self.request.return_value.raw.seek(0)
        self.request.return_value._content_consumed = False

        expect(os.path.isfile('path_to_file')).is_False()
        expect(self.repo.archive('tarball', 'path_to_file')).is_True()
        expect(os.path.isfile('path_to_file')).is_True()
        os.unlink('path_to_file')

        self.request.return_value.raw.seek(0)
        self.request.return_value._content_consumed = False

        self.get(self.api + 'zipball/randomref')
        expect(self.repo.archive('zipball', ref='randomref')).is_True()
        os.unlink('foo')

        self.request.return_value.raw.seek(0)
        self.request.return_value._content_consumed = False

        o = mock_open()
        with patch('{0}.open'.format(__name__), o, create=True):
            with open('archive', 'wb+') as fd:
                self.repo.archive('tarball', fd)

        o.assert_called_once_with('archive', 'wb+')
        fd = o()
        fd.write.assert_called_once_with(b'archive_data')

We start this test by setting up headers that are set by GitHub when returning 
data like an archive. We then pass those headers to the Response constructor 
and set the url. We're also expecting that github3.py is going to pass 
``stream=True`` to the request. We then finally make a request and test the 
assertions about the mock. That resets the mock and then we can go on to test 
the other features of the ``archive`` method. At the end, we mock the built-in 
``open`` method, but that's covered in the mock documentation.

.. _expecter: http://expecter-gadget.rtfd.org
.. _mock: http://mock.rtfd.org
