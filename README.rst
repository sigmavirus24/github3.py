github3.py
==========

Eventually this will be a python module to access the GitHub v3 API.

Easy Cloning
------------

Assuming you have git 1.7.x (although I'm not entirely certain what version
it was introduced in) you can perform ``git clone --recursive
git://github.com/sigmavirus24/github3.py.git github3.py`` to clone this 
and the submodule at the same time. Otherwise you have to do:

::

    $ git clone git://github.com/sigmavirus24/github3.py.git
    $ cd github3.py
    $ git submodule init
    $ git submodule update

Dependencies
------------

- requests_  by Kenneth Reitz
  
.. _requests: https://github.com/kennethreitz/requests

Progress
--------

- Gists_: **done**

  - `Comments <http://developer.github.com/v3/gists/comments/>`_: **done**

- `Git Data`_

  - Blobs_

  - `Commits <http://developer.github.com/v3/events/>`_

  - References_

  - Tags_

  - Trees_

- Issues_: **in progress**

  - `Comments <http://developer.github.com/v3/issues/comments/>`_

  - `Events <http://developer.github.com/v3/issues/events/>`_

  - Labels_

  - Milestones_

- Organizations_

  - Members_

  - Teams_

- `Pull Requests`_

  - `Review Comments`_

- Repositories_

  - Collaborators_

  - `Commits <http://developer.github.com/v3/repos/commits/>`_

  - Downloads_

  - Forks_

  - Keys_

  - Watching_

  - Hooks_

- Users_

  - Emails_

  - Followers_

  - `Keys <http://developer.github.com/v3/users/keys/>`_

- Events_

  - Types_

.. Links
.. _Gists: http://developer.github.com/v3/gists/
.. _Git Data: http://developer.github.com/v3/git/
.. _Blobs: http://developer.github.com/v3/git/blobs/
.. _References: http://developer.github.com/v3/git/refs/
.. _Tags: http://developer.github.com/v3/git/tags/
.. _Trees: http://developer.github.com/v3/git/trees/
.. _Issues: http://developer.github.com/v3/issues/
.. _Labels: http://developer.github.com/v3/issues/labels/
.. _Milestones: http://developer.github.com/v3/issues/milestones/
.. _Organizations: http://developer.github.com/v3/orgs/
.. _Members: http://developer.github.com/v3/orgs/members/
.. _Teams: http://developer.github.com/v3/orgs/teams/
.. _Pull Requests: http://developer.github.com/v3/pulls/
.. _Review Comments: http://developer.github.com/v3/pulls/comments/
.. _Repositories: http://developer.github.com/v3/repos/
.. _Collaborators: http://developer.github.com/v3/repos/collaborators/
.. _Downloads: http://developer.github.com/v3/repos/downloads/
.. _Forks: http://developer.github.com/v3/repos/forks/
.. _Keys: http://developer.github.com/v3/repos/keys/
.. _Watching: http://developer.github.com/v3/repos/watching/
.. _Hooks: http://developer.github.com/v3/repos/hooks/
.. _Users: http://developer.github.com/v3/users/
.. _Emails: http://developer.github.com/v3/users/emails/
.. _Followers: http://developer.github.com/v3/users/followers/
.. _Events: http://developer.github.com/v3/events/
.. _Types: http://developer.github.com/v3/events/types/

License
-------

Modified BSD license_

.. _license:

Examples
--------

::

  >>> from github3 import login
  >>> gh = login(username, password)
  >>> gists = gh.gists()
  >>> files = {'spam.txt' : {'content': 'What... is the air-speed velocity of an
  unladen swallow?'}}
  >>> gh.create_gist('Answer this to cross the bridge', files, public=False)
  <Gist [gist-id]>

::

  >>> from github3 import create_gist
  >>> files = {'spam.txt' : {'content': 'What... is the air-speed velocity of an
  unladen swallow?'}}
  >>> gist = create_gist('Answer this to cross the bridge', files, public=False)
  >>> gist.list_comments()
  []
  >>> gist.create_comment('Bogus. This will not work.')
  # Which of course it didn't, because you're not logged in

::

  >>> from github3 import login
  >>> gh = login(username, password)
  >>> issue = gh.issue('sigmavirus24', 'issues.py', 2)
  >>> issue.html_url
  u'https://github.com/sigmavirus24/issues.py/issues/2'
  >>> issue.state
  u'open'
  >>> issue.close()
  True
  >>> issue.reopen()
  True
  >>> issue.edit('Testing Github3.py', 'Testing re-opening', 'sigmavirus24')
  True

Author
------

Sigmavirus24
