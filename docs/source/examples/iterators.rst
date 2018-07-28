.. _iteratorex:

Taking Advantage of GitHubIterator
==================================

Let's say that for some reason you're stalking all of GitHub's users and you
just so happen to be using github3.py to do this. You might write code that
looks like this:

.. code-block:: python

    import github3

    g = github3.login(USERNAME, PASSWORD)

    for u in g.iter_all_users():
        add_user_to_database(u)

The problem is that you will then have to reiterate over all of the users each
time you want to get the new users. You have two approaches you can take to
avoid this with :class:`GitHubIterator <github3.structs.GitHubIterator>`.

You can not call the method directly in the for-loop and keep the iterator as
a separate reference like so:

.. code-block:: python

    i = g.iter_all_users():

    for u in i:
        add_user_to_database(u)

The First Approach
------------------

Then after your first pass through your ``GitHubIterator`` object will have an
attribute named ``etag``. After you've added all the currently existing users
you could do the following to retrieve the new users in a timely fashion:

.. code-block:: python

    import time

    while True:
        i.refresh(True)
        for u in i:
            add_user_to_database(u)

        time.sleep(120)  # Sleep for 2 minutes

The Second Approach
-------------------

.. code-block:: python

    etag = i.etag
    # Store this somewhere

    # Later when you start a new process or go to check for new users you can
    # then do

    i = g.iter_all_users(etag=etag)

    for u in i:
        add_user_to_database(u)

------

If there are no new users, these approaches won't impact your rate limit at
all. This mimics the ability to conditionally refresh data on almost all other
objects in github3.py.
