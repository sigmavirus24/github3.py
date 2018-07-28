=================
 Getting Started
=================

This chapter in our documentation will teach you how to get started using
github3.py after you've installed the library.


Using the library
-----------------

To get started using the library, it's important to note that the module that
is provided by this library is called ``github3``. To use it you can run:

.. code-block:: python

    import github3

where necessary.


.. _logging-in:

Logging into GitHub using github3.py
------------------------------------

Once you've imported the module, you can get started using the API. It's
recommended that you authenticate with GitHub to avoid running into `their
rate limits`_. To do so you have a few options.

First, you can use your username and password. We advise you not to type your
password into your shell or python console directly as others can view that
after the fact. For the sake of an example, let's assume that you have two
variables bound as ``username`` and ``password`` that contain your username
and password. You can then do:

.. code-block:: python

    import github3

    github = github3.login(username=username, password=password)

Second, you can `generate an access token`_ and use that. Let's presume you
have a variable bound as ``token`` that contains your access token.

.. code-block:: python

    import github3

    github = github3.login(token=token)

Third, if you're using a GitHub Enterprise installation you can use similar
methods above, but you'll need to use :func:`~github3.api.enterprise_login`,
e.g.,

.. code-block:: python

    import github3

    githubent = github3.enterprise_login(
        url='https://github.myenterprise.example.com',
        username=username,
        password=password,
    )

    githubent = github3.enterprise_login(
        url='https://github.myenterprise.example.com',
        token=token,
    )


Two-Factor Authentication and github3.py
----------------------------------------

GitHub has long supported the use of a second-factor authentication (a.k.a,
2FA) mechanism for logging in. This provides some extra security, especially
around administrative actions on the website. If you choose to login with
simply your username and password and you have to provide github3.py with a
mechanism for obtaining your token and providing it to GitHub.

An example mechanism is as follows:

.. code-block:: python

    # This assumes Python 3
    import github3


    def second_factor_retrieval():
        """Provide a way to retrieve the code from the user."""
        code = ''
        while not code:
            code = input('Enter 2FA code: ')
        return code


    github = github3.login(username, password,
                           two_factor_callback=second_factor_retrieval)


This means that for every API call made, GitHub will force us to prompt you
for a new 2FA code. This is obviously not ideal. In those situations, you
almost certainly want to obtain an access token.


.. links
.. _their rate limits:
    https://developer.github.com/v3/#rate-limiting
.. _generate an access token:
    https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/
