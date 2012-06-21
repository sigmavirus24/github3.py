.. _github:

GitHub Examples
===============

Examples using the GitHub object.

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

For the cases where we do not need an authenticated user, or where we are trying
to demonstrate the differences between the two, I will use ``anon``. ``anon``
could be instantiated like so::

    anon = GitHub()
    

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
        key = g.create_key(name, key_file):
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
