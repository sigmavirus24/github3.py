History/Changelog
=================

0.5: 2013-02-16
---------------

- 100% (mock) test coverage

- Add support for the announced_ meta_ endpoint.

- Add support for conditional refreshing, e.g.,

  ::

      import github3

      u = github3.user('sigmavirus24')

      # some time later

      u.refresh()  # Will ALWAYS send a GET request and lower your ratelimit
      u.refresh(True)  # Will send the GET with a header such that if nothing
                       # has changed, it will not count against your ratelimit
                       # otherwise you'll get the updated user object.

- Add support for conditional iterables. What this means is that you can do:

  ::

      import github3

      i = github3.iter_all_repos(10)

      for repo in i:
          # do stuff

      i = github3.iter_all_repos(10, etag=i.etag)

  And the second call will only give you the new repositories since the last 
  request. This mimics behavior in `pengwynn/octokit`_

- Add support for `sortable stars`_.

- In github3.users.User, ``iter_keys`` now allows you to iterate over **any** 
  user's keys. No name is returned for each key. This is the equivalent of 
  visiting: github.com/:user.keys

- In github3.repos.Repository, ``pubsubhubbub`` has been removed. Use 
  github3.github.Github.pubsubhubbub instead

- In github3.api, ``iter_repo_issues``'s signature has been corrected.

- Remove ``list_{labels, comments, events}`` methods from github3.issues.Issue

- Remove ``list_{comments, commits, files}`` methods from 
  github3.pulls.PullRequest

- In github3.gists.Gist:

  - the ``user`` attribute was changed by GitHub and is now the ``owner`` 
    attribute

  - the ``public`` attribute and the ``is_public`` method return the same 
    information. The method will be removed in the next version.

  - the ``is_starred`` method now requires authentication

  - the default ``refresh`` method is no longer over-ridden. In a change made 
    in before, a generic ``refresh`` method was added to most objects. This 
    was overridden in the Gist object and would cause otherwise unexpected 
    results.

- ``github3.events.Event.is_public()`` and ``github3.events.Event.public`` now 
  return the same information. In the next version, the former will be 
  removed.

- In github3.issues.Issue

   - ``add_labels`` now returns the list of Labels on the issue instead of a 
     boolean.

   - ``remove_label`` now retuns a boolean.

   - ``remove_all_labels`` and ``replace_labels`` now return lists. The former 
     should return an empty list on a successful call. The latter should 
     return a list of ``github3.issue.Label`` objects.

- Now we won't get spurious GitHubErrors on 404s, only on other expected 
  errors whilst accessing the json in a response. All methods that return an 
  object can now *actually* return None if it gets a 404 instead of just 
  raising an exception. (Inspired by #49)

- GitHubStatus API now works.

.. _announced: https://github.com/blog/1402-upcoming-changes-to-github-services
.. _meta: http://developer.github.com/v3/meta/
.. _sortable stars:
    http://developer.github.com/changes/2013-2-13-sortable-stars/
.. _pengwynn/octokit: https://github.com/pengwynn/octokit

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
