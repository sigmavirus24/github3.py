History/Changelog
=================

0.4: 2013-01-16
---------------

- In github3.legacy.LegacyRepo

  - ``has_{downloads,issues,wiki}`` are now attributes.
  - ``is_private()`` and the ``private`` attribute return the same thing 
    ``is_private()`` will be deprecated in the next release.

- In github3.repos.Repository

  - ``is_fork()`` is now deprecated in favor of the ``fork`` attribute
  - ``is_private()`` is now deprecated in favor of the ``private`` attribute

- In github3.repos.Hook

  - ``is_active()`` is now deprecated in favor of the ``active`` attribute

- In github3.pulls.PullRequest

  - ``is_mergeable()`` is now deprecated in favor of the ``mergeable`` 
    attribute

- In github3.notifications.Thread

  - ``is_unread()`` is now deprecated in favor of the ``unread``

- ``pubsubhubbub()`` is now present on the ``GitHub`` object and will be 
  removed from the ``Repository`` object in the next release

- 70% test coverage

0.3: 2013-01-01
---------------

- In github3.repos.Repository

  - is_fork() and fork return the same thing
  - is_private() and private return the same thing as well
  - has_downloads, has_issues, has_wiki are now straight attributes

- In github3.repos.Hook

  - is_active() and active return the same value

- In github3.pulls.PullRequest

  - is_mergeable() and mergeable are now the same
  - repository now returns a tuple of the login and name of the repository it 
    belongs to

- In github3.notifications.Thread

  - is_unread() and unread are now the same

- In github3.gists

  - GistFile.filename and GistFile.name return the same information
  - Gist.history now lists the history of the gist
  - GistHistory is an object representing one commit or version of the history
  - You can retrieve gists at a specific version with GistHistory.get_gist()

- github3.orgs.Organization.iter_repos now accepts all types_

- list_* methods on Organization objects that were missed are now deleted

- Some objects now have ``__str__`` methods. You can now do things like:

  ::

    import github3
    u = github3.user('sigmavirus24')
    r = github3.repository(u, 'github3.py')

  And

  ::

    import github3

    r = github3.repository('sigmavirus24', 'github3.py')

    template = """Some kind of template where you mention this repository 
    {0}"""

    print(template.format(r))
    # Some kind of template where you mention this repository
    # sigmavirus24/github3.py

  Current list of objects with this feature:

  - github3.users.User (uses the login name)
  - github3.users.Key (uses the key text)
  - github3.users.Repository (uses the login/name pair)
  - github3.users.RepoTag (uses the tag name)
  - github3.users.Contents (uses the decoded content)

- 60% test coverage with mock
- Upgrade to requests 1.0.x

.. _types: http://developer.github.com/v3/repos/#list-organization-repositories

0.2: 2012-11-21
---------------

- MAJOR API CHANGES:

  - ``GitHub.iter_subscribed`` --> ``GitHub.iter_subscriptions``
  - Broken ``list_*`` functions in github3.api have been renamed to the correct
    ``iter_*`` methods on ``GitHub``.
  - Removed ``list_*`` functions from ``Repository``, ``Gist``,
    ``Organization``, and ``User`` objects

- Added zen of GitHub method.
- More tests
- Changed the way ``Repository.edit`` works courtesy of Kristian Glass
  (@doismellburning)
- Changed ``Repository.contents`` behaviour when acting on a 404.
- 50% test coverage via mock tests

0.1: 2012-11-13
---------------

- Add API for GitHub Enterprise customers.

0.1b2: 2012-11-10
-----------------

- Handle 500 errors better, courtesy of Kristian Glass (@doismellburning)
- Handle sending json with `%` symbols better, courtesy of Kristian Glass
- Correctly handle non-GitHub committers and authors courtesy of Paul Swartz 
  (@paulswartz)
- Correctly display method signatures in documentation courtesy of (@seveas)

0.1b1: 2012-10-31
-----------------

- unit tests implemented using mock instead of hitting the GitHub API (#37)
- removed ``list_*`` functions from GitHub object
- Notifications API coverage

0.1b0: 2012-10-06
-----------------

- Support for the complete GitHub API (accomplished)

  - Now also includes the Statuses API
  - Also covers the auto_init parameters to the Repository creation 
    methodology
  - Limited implementation of iterators in the place of list functions.

- 98% coverage by unit tests
