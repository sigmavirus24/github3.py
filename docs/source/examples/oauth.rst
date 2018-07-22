.. _oauth:

Using Tokens for Your Projects
------------------------------

Let's say you're designing an application that uses github3.py. If your
intention is to have users authenticate, you have a few options.

1. Ask the user to enter their credentials each time they start the
   application. (Or save the username somewhere, and just ask for the
   password.)
2. Ask the user to supply their credentials once and store them somewhere for
   later use.
3. Ask the user to supply their credentials once, get an authorization token
   and store that for later use.

The first isn't a bad method at all, it just unfortunately may lead to unhappy
users, this should always be an option though. The second (as I already noted)
is a bad idea. Even if you obfuscate the username and password, they can still
be discovered and no level of obfuscation is clever enough. (May I also take
this moment to remind people that base64 is **not** encryption.) The last is
probably the least objectionable of the evils. The token has scopes so there
is only so much someone can do with it and it works well with github3.py.

Requesting a token
~~~~~~~~~~~~~~~~~~

If you're not doing a web application, you are more than welcome to use
github3.py (otherwise work with redirects_). Let's say your application needs
access to public and private repositories, and the users but not to gists.
Your scopes_ should be ``['user', 'repo']``. I'm also assuming your
application will not be deleting any repositories. The only things left to do
are collect the username and password and give a good description for your
application.

::

    from github3 import authorize
    from getpass import getuser, getpass

    user = getuser()
    password = ''

    while not password:
        password = getpass('Password for {0}: '.format(user))

    note = 'github3.py example app'
    note_url = 'http://example.com'
    scopes = ['user', 'repo']

    auth = authorize(user, password, scopes, note, note_url)

    with open(CREDENTIALS_FILE, 'w') as fd:
        fd.write(auth.token + '\n')
        fd.write(auth.id)

In the future, you can then read that token in without having to bother your
user. If at some later point in the lifetime of your application you need more
privileges, you simply do the following:

::

    from github3 import login

    token = id = ''
    with open(CREDENTIALS_FILE, 'r') as fd:
        token = fd.readline().strip()  # Can't hurt to be paranoid
        id = fd.readline().strip()

    gh = login(token=token)
    auth = gh.authorization(id)
    auth.update(add_scopes=['repo:status', 'gist'], rm_scopes=['user'])

    # if you want to be really paranoid, you can then test:
    # token == auth.token
    # in case the update changes the token

.. _redirects: http://developer.github.com/v3/oauth/#redirect-urls
.. _scopes: http://developer.github.com/v3/oauth/#scopes
