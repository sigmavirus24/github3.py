.. _gistex:

Gist Code Examples
==================

Examples with :class:`Gist <github3.gist.Gist>`\ s


Listing gists after authenticating
----------------------------------

::

    from github3 import login

    gh = login(username, password)
    gists = [g for g in gh.iter_gists()]

Creating a gist after authenticating
------------------------------------

::

    from github3 import login

    gh = login(username, password)
    files = {
        'spam.txt' : {
            'content': 'What... is the air-speed velocity of an unladen swallow?'
            }
        }
    gist = gh.create_gist('Answer this to cross the bridge', files, public=False)
    # gist == <Gist [gist-id]>
    print(gist.html_url)


Creating an anonymous gist
--------------------------

::

    from github3 import create_gist

    files = {
        'spam.txt' : {
            'content': 'What... is the air-speed velocity of an unladen swallow?'
            }
        }
    gist = create_gist('Answer this to cross the bridge', files)
    comments = [c for c in gist.iter_comments()]
    # []
    comment = gist.create_comment('Bogus. This will not work.')
    # Which of course it didn't, because you're not logged in
    # comment == None
    print(gist.html_url)

In the above examples ``'spam.txt'`` is the file name. GitHub will autodetect
file type based on extension provided. ``'What... is the air-speed velocity of
an unladen swallow?'`` is the file's content or body. ``'Answer this to cross
the bridge'`` is the gist's description. While required by github3.py, it is
allowed to be empty, e.g., ``''`` is accepted by GitHub.

Note that anonymous gists are always public.
