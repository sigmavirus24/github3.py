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

  - `Gist Comments`_: **done**

.. _Gists: http://developer.github.com/v3/gists/
.. _Gist Comments: http://developer.github.com/v3/gists/comments/

- `Git Data`_: **done**

  - Blobs_: **done**

  - Commits_: **done**

  - References_: **done**

  - Tags_: **done**

  - Trees_: **done**

.. _Git Data: http://developer.github.com/v3/git/
.. _Commits: http://developer.github.com/v3/events/
.. _Blobs: http://developer.github.com/v3/git/blobs/
.. _References: http://developer.github.com/v3/git/refs/
.. _Tags: http://developer.github.com/v3/git/tags/
.. _Trees: http://developer.github.com/v3/git/trees/

- Issues_: **done**

  - `Issue Comments`_: **done**

  - `Issue Events`_: **done**

  - Labels_: **done**

  - Milestones_: **done**

.. _Issues: http://developer.github.com/v3/issues/
.. _Issue Comments: http://developer.github.com/v3/issues/comments/>
.. _Issue Events: http://developer.github.com/v3/issues/events/
.. _Labels: http://developer.github.com/v3/issues/labels/
.. _Milestones: http://developer.github.com/v3/issues/milestones/

- Organizations_: **done**

  - Members_: **done**

  - Teams_: **done**

.. _Organizations: http://developer.github.com/v3/orgs/
.. _Members: http://developer.github.com/v3/orgs/members/
.. _Teams: http://developer.github.com/v3/orgs/teams/

- `Pull Requests`_: **done*

  - `Review Comments`_: **done**

.. _Pull Requests: http://developer.github.com/v3/pulls/
.. _Review Comments: http://developer.github.com/v3/pulls/comments/

- Repositories_

  - Collaborators_

  - `Repo Commits`_

  - Downloads_

  - Forks_

  - `Repo Keys`_

  - Watching_

  - Hooks_

.. _Repositories: http://developer.github.com/v3/repos/
.. _Collaborators: http://developer.github.com/v3/repos/collaborators/
.. _Repo Commits: http://developer.github.com/v3/repos/commits/
.. _Downloads: http://developer.github.com/v3/repos/downloads/
.. _Forks: http://developer.github.com/v3/repos/forks/
.. _Repo Keys: http://developer.github.com/v3/repos/keys/
.. _Watching: http://developer.github.com/v3/repos/watching/
.. _Hooks: http://developer.github.com/v3/repos/hooks/

- Users_: **done**

  - Emails_: **done**

  - Followers_: **done**

  - `User Keys`_: **done**

.. _Users: http://developer.github.com/v3/users/
.. _Emails: http://developer.github.com/v3/users/emails/
.. _Followers: http://developer.github.com/v3/users/followers/
.. _User Keys: http://developer.github.com/v3/users/keys/

- Events_: **started/postponed**

  - Types_: **started/postponed**

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
  >>> gists = gh.list_gists()
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

::

  >>> from github3 import login
  >>> gh = login(username, password)
  >>> issue = gh.issue('sigmavirus24', 'Todo.txt-python', 17)
  >>> issue.html_url
  u'https://github.com/sigmavirus24/Todo.txt-python/issues/17'
  >>> issue.state
  u'open'
  >>> events = issue.list_events()
  >>> events
  [<Issue Event [#17 - subscribed - sigmavirus24]>, <Issue Event [#17 - assigned - sigmavirus24]>,
   <Issue Event [#17 - referenced - sigmavirus24]>]
  >>> events[0].actor
  <User [sigmavirus24:None]>
  >>> events[0].issue
  <Issue [sigmavirus24/Todo.txt-python #17]>
  >>> events[0].closed_at
  >>> events[0].event
  u'subscribed'

::

  >>> from github3 import login
  >>> g = login(username, password)
  >>> repo = g.repository('sigmavirus24', 'Todo.txt-python')
  >>> sha = repo.create_blob('Testing blob creation', 'utf-8')
  >>> sha
  u'57fad9a39b27e5eb4700f66673ce860b65b93ab8'
  >>> blob = repo.blob(sha)
  >>> blob.content
  u'VGVzdGluZyBibG9iIGNyZWF0aW9u\n'
  >>> blob.decoded
  u'Testing blob creation'
  >>> blob.encoding
  u'base64'

::

  >>> from github3 import login
  >>> g = login(username, password)
  >>> repo = g.repository('sigmavirus24', 'github3.py')
  >>> tag = repo.tag('cdba84b4fede2c69cb1ee246b33f49f19475abfa')
  >>> tag
  <Tag [cdba84b4fede2c69cb1ee246b33f49f19475abfa]>
  >>> tag.object.sha
  u'24ea44d302c6394a0372dcde8fd8aed899c0034b'
  >>> tag.object.type
  u'commit'

Author
------

Sigmavirus24
