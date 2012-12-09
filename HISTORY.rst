History/Changelog
=================

0.3: xxxx-xx-xx
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
