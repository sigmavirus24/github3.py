Users
-----

`http://developer.github.com/v3/users/ <http://developer.github.com/v3/users/>`_

.. toctree::
    :maxdepth: 1

    users/emails
    users/followers
    users/public-keys


Get a single user
~~~~~~~~~~~~~~~~~

`http://developer.github.com/v3/users/#get-a-single-user <http://developer.github.com/v3/users/#get-a-single-user>`_


Get the authenticated user
~~~~~~~~~~~~~~~~~~~~~~~~~~

`http://developer.github.com/v3/users/#get-the-authenticated-user <http://developer.github.com/v3/users/#get-the-authenticated-user>`_

Update the authenticated user
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`http://developer.github.com/v3/users/#update-the-authenticated-user <http://developer.github.com/v3/users/#update-the-authenticated-user>`_

Get all users
~~~~~~~~~~~~~

`http://developer.github.com/v3/users/#get-all-users <http://developer.github.com/v3/users/#get-all-users>`_


If you want a list of all users in order they signed up to GitHub, use:


.. autofunction:: github3.iter_all_users
    :noindex:


An Example:

.. code-block:: python
        
        In [1]: import github3

        In [2]: users = github3.iter_all_users()

        In [3]: type(users)
        Out[3]: github3.structs.GitHubIterator

        In [4]: user = users.next()

        In [5]: type(user)
        Out[5]: github3.users.User

        In [6]: user.html_url
        Out[6]: u'https://github.com/mojombo'





