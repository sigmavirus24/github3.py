Writing Tests for github3.py
============================

Unit Tests
----------

    In computer programming, unit testing is a method by which individual
    units of source code, sets of one or more computer program modules
    together with associated control data, usage procedures, and operating
    procedures are tested to determine if they are fit for use. Intuitively,
    one can view a unit as the smallest testable part of an application.

    -- `Unit Testing on Wikipedia
    <http://en.wikipedia.org/wiki/Unit_testing>`_

In github3.py we use unit tests to make assertions about how the library
behaves without making a request to the internet. For example, one assertion
we might write would check if custom information is sent along in a request to
GitHub.

An existing test like this can be found in
``tests/unit/test_repos_release.py``:

.. code:: python

    def test_delete(self):
        self.instance.delete()
        self.session.delete.assert_called_once_with(
            self.example_data['url'],
            headers={'Accept': 'application/vnd.github.manifold-preview'}
        )

In this test, we check that the library passes on important headers to the API
to ensure the request will work properly. ``self.instance`` is created for us
and is an instance of the ``Release`` class. The test then calls ``delete`` to
make a request to the API. ``self.session`` is a mock object which fakes out a
normal session. It does not allow the request through but allows us to verify
how github3.py makes a request. We can see that github3.py called ``delete``
on the session. We assert that it was only called once and that the only
parameters sent were a URL and the custom headers that we are concerned with.

Mocks
~~~~~

Above we talked about mock objects. What are they?

    In object-oriented programming, mock objects are simulated objects that
    mimic the behavior of real objects in controlled ways. A programmer
    typically creates a mock object to test the behavior of some other object,
    in much the same way that a car designer uses a crash test dummy to
    simulate the dynamic behavior of a human in vehicle impacts.

    -- `Mock Object on Wikipedia <http://en.wikipedia.org/wiki/Mock_object>`_

We use mocks in github3.py to prevent the library from talking directly with
GitHub. The mocks we use intercept requests the library makes so we can verify
the parameters we use. In the example above, we were able to check that
certain parameters were the only ones sent to a session method because we
mocked out the session.

You may have noticed in the example above that we did not have to set up the
mock object. There is a convenient helper written in ``tests/unit/helper.py``
to do this for you.

Example - Testing the Release Object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here's a full example of how we test the ``Release`` object in
``tests/unit/test_repos_release.py``.

Our first step is to import the ``UnitHelper`` class from
``tests/unit/helper.py`` and the ``Release`` object from
``github3/repos/release.py``.

.. code:: python

    from .helper import UnitHelper
    from github3.repos.release import Release

Then we construct our test class and indicate which class we will be testing
(or describing).

.. code:: python

    class TestRelease(UnitHelper):
        described_class = Release

We can then use the `GitHub API documentation about Releases
<http://developer.github.com/v3/repos/releases/>`_ to retrieve example release
data. We then can use that as example data for our test like so:

.. code:: python

    class TestRelease(UnitHelper):
        described_class = Release
        example_data = {
            "url": releases_url("/1"),
            "html_url": "https://github.com/octocat/Hello-World/releases/v1.0.0",
            "assets_url": releases_url("/1/assets"),
            "upload_url": releases_url("/1/assets{?name}"),
            "id": 1,
            "tag_name": "v1.0.0",
            "target_commitish": "master",
            "name": "v1.0.0",
            "body": "Description of the release",
            "draft": False,
            "prerelease": False,
            "created_at": "2013-02-27T19:35:32Z",
            "published_at": "2013-02-27T19:35:32Z"
            }

The above code now will handle making clean and brand new instances of the
``Release`` object with the example data and a faked out session. We can now
construct our first test.

.. code:: python

    def test_delete(self):
        self.instance.delete()
        self.session.delete.assert_called_once_with(
            self.example_data['url'],
            headers={'Accept': 'application/vnd.github.manifold-preview'}
        )


Integration Tests
-----------------

    Integration testing is the phase in software testing in which individual
    software modules are combined and tested as a group.

    The purpose of integration testing is to verify functional, performance,
    and reliability requirements placed on major design items.

    -- `Integration tests on Wikipedia
    <http://en.wikipedia.org/wiki/Integration_tests>`_

In github3.py we use integration tests to ensure that when we make what should
be a valid request to GitHub, it is in fact valid. For example, if we were
testing how github3.py requests a user's information, we would expect a
request for a real user's data to be valid. If the test fails we know either
what the library is doing is wrong or the data requested does not exist.

An existing test that demonstrates integration testing can be found in
``tests/integration/test_repos_release.py``:

.. code:: python

    def test_iter_assets(self):
        """Test the ability to iterate over the assets of a release."""
        cassette_name = self.cassette_name('iter_assets')
        with self.recorder.use_cassette(cassette_name):
            repository = self.gh.repository('sigmavirus24', 'github3.py')
            release = repository.release(76677)
            for asset in release.iter_assets():
                assert isinstance(asset, github3.repos.release.Asset)
            assert asset is not None

In this test we use ``self.recorder`` to record our interaction with GitHub.
We then proceed to make the request to GitHub that will exercise the code we
wish to test. First we request a ``Repository`` object from GitHub and then
using that we request a ``Release`` object. After receiving that release, we
exercise the code that lists the assets of a ``Release``. We verify that each
asset is an instance of the ``Asset`` class and that at the end the ``asset``
variable is not ``None``. If ``asset`` was ``None``, that would indicate that
GitHub did not return any data and it did not exercise the code we are trying
to test.

Betamax
~~~~~~~

Betamax_ is the library that we use to create the recorder above. It sets up
the session object to intercept every request and corresponding response and
save them to what it calls cassettes_. After you record the interaction it
never has to speak to the internet again for that request.

In github3.py there is a helper class (much like ``UnitHelper``) in
``tests/integration/helper.py`` which sets everything up for us.

Example - Testing the Release Object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here's an example of how we write an integration test for github3.py. The
example can be found in ``tests/integration/test_repos_release.py``.

Our first steps are the necessary imports.

.. code:: python

    import github3

    from .helper import IntegrationHelper


Then we start writing our test right away.

.. code:: python

    class TestRelease(IntegrationHelper):
        def test_delete(self):
            """Test the ability to delete a release."""
            self.token_login()
            cassette_name = self.cassette_name('delete')
            with self.recorder.use_cassette(cassette_name):
                repository = self.gh.repository('github3py', 'github3.py')
                release = repository.create_release(
                    '0.8.0.pre', 'develop', '0.8.0 fake release',
                    'To be deleted'
                    )
                assert release is not None
                assert release.delete() is True

Every test has access to ``self.gh`` which is an instance of ``GitHub``.
``IntegrationHelper`` provides a lot of methods that allow you to focus on
what we are testing instead of setting up for the test. The first of those
methods we see in use is ``self.token_login`` which handles authenticating
with a token. It's sister method is ``self.basic_login`` which handles
authentication with basic credentials. Both of these methods will set up the
authentication for you on ``self.gh``.

The next convenience method we see is ``self.cassette_name``. It constructs a
cassette name for you based on the test class name and the string you provide
it.

Every test also has access to ``self.recorder``. This is the Betamax recorder
that has been set up for you to record your interactions. The recorder is
started when you write

.. code:: python

    with self.recorder.use_cassette(cassette_name):
        # ...

Everything that talks to GitHub should be written inside of the context
created by the context manager there. No requests to GitHub should be made
outside of that context.

In that context, we then retrieve a repository and create a release for it. We
want to be sure that we will be deleting something that exists so we assert
that what we received back from GitHub is not ``None``. Finally we call
``delete`` and assert that it returns ``True``.

When you write your new test and record a new cassette, be sure to add the new
cassette file to the repository, like so:

.. code::

    git add tests/cassettes/Release_delete.json

Recording Cassettes that Require Authentication/Authorization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you need to write a test that requires an Authorization (i.e., OAuth token)
or Authentication (i.e., username and password), all you need to do is set
environment variables when running `py.test`, e.g.,

.. code::

    GH_AUTH="abc123" py.test
    GH_USER="sigmavirus24" GH_PASSWORD="super-secure-password-plz-kthxbai" py.test

If you are concerned that your credentials will be saved, you need not worry.
Betamax sanitizes information like that before saving the cassette. It never
does hurt to double check though.

.. _Betamax: https://github.com/sigmavirus24/betamax
.. _cassettes: https://betamax.readthedocs.io/en/latest/cassettes.html
