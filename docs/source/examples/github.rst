.. _github_examples:

GitHub Examples
===============

Examples using the :class:`GitHub <github3.github.GitHub>` object.

Assumptions
-----------

I'll just make some basic assumptions for the examples on this page. First,
let's assume that all you ever import from github3.py is ``login`` and
``GitHub`` and that you have already received your :class:`GitHub <GitHub>`
object ``g``. That might look like this::

    from github3 import login, GitHub
    from getpass import getpass, getuser
    import sys
    try:
        import readline
    except ImportError:
        pass

    try:
        user = raw_input('GitHub username: ')
    except KeyboardInterrupt:
        user = getuser()

    password = getpass('GitHub password for {0}: '.format(user))

    # Obviously you could also prompt for an OAuth token
    if not (user and password):
        print("Cowardly refusing to login without a username and password.")
        sys.exit(1)

    g = login(user, password)

So anywhere you see ``g`` used, you can safely assume that it is an instance
where a user has authenticated already.

For the cases where we do not need an authenticated user, or where we are
trying to demonstrate the differences between the two, I will use ``anon``.
``anon`` could be instantiated like so::

    anon = GitHub()

Also let's define the following constants::

    sigma = 'sigmavirus24'
    github3 = 'github3.py'
    todopy = 'Todo.txt-python'
    kr = 'kennethreitz'
    requests = 'requests'

We may not need all of them, but they'll be useful

Adding a new key to your account
--------------------------------

::

    try:
        path = raw_input('Path to key: ')
    except KeyboardInterrupt:
        path = ''

    try:
        name = raw_input('Key name: ')
    except KeyboardInterrupt:
        name = ''

    if not (path and name):  # Equivalent to not path or not name
        print("Cannot create a new key without a path or name")
        sys.exit(1)

    with open(path, 'r') as key_file:
        key = g.create_key(name, key_file)
        if key:
            print('Key {0} created.'.format(key.title))
        else:
            print('Key addition failed.')


Deleting the key we just created
--------------------------------

Assuming we still have ``key`` from the previous example:

::

    if g.delete_key(key.id):
        print("Successfully deleted key {0}".format(key.id))

There would actually be an easier way of doing this, however, if we do have the
``key`` object that we created:

::

    if key.delete():
        print("Successfully deleted key {0}".format(key.id))

Creating a new repository
-------------------------

::

    repo = {}
    keys = ['name', 'description', 'homepage', 'private', 'has_issues',
        'has_wiki', 'has_downloads']

    for key in keys:
        try:
            repo[key] = raw_input(key + ': ')
        except KeyboardInterrupt:
            pass

    r = None
    if repo.get('name'):
        r = g.create_repo(repo.pop('name'), **repo)

    if r:
        print("Created {0} successfully.".format(r.name))

Create a commit to change an existing file
------------------------------------------

::

    repo.contents('/README.md').update('commit message', 'file content'.encode('utf-8'))

Follow another user on GitHub
-----------------------------

I'm cheating here and using most of the follow functions in one example

::

    if not g.is_following(sigma):
        g.follow(sigma)

    if not g.is_subscribed(sigma, github3py):
        g.subscribe(sigma, github3py)

    if g.is_subscribed(sigma, todopy):
        g.unsubscribe(sigma, todopy)

    for follower in g.iter_followers():
        print("{0} is following me.".format(follower.login))

    for followee in g.iter_following():
        print("I am following {0}.".format(followee.login))

    if g.is_following(sigma):
        g.unfollow(sigma)

Changing your user information
------------------------------

Note that you **can not** change your login name via the API.

::

    new_name = 'J. Smith'
    blog = 'http://www.example.com/'
    company = 'Vandelay Industries'
    bio = """# J. Smith

    A simple man working at a latex factory
    """

    if g.update_user(new_name, blog, company, bio=bio):
        print('Profile updated.')

This is the same as::

    me = g.me() # or me = g.user(your_user_name)
    if me.update(new_name, blog, company, bio=bio):
        print('Profile updated.')
