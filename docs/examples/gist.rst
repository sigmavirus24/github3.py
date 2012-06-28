.. _gistex:

Gist Code Examples
==================

Examples with :class:`Gist <github3.gist.Gist>`\ s


Listing gists after authenticating
----------------------------------

::

    from github3 import login

    gh = login(username, password)
    gists = gh.list_gists()

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
    gist = create_gist('Answer this to cross the bridge', files, public=False)
    gist.list_comments()
    # []
    comment = gist.create_comment('Bogus. This will not work.')
    # Which of course it didn't, because you're not logged in
    # comment == None
    print(gist.html_url)
