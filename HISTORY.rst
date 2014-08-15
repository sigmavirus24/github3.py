.. vim: set tw=100

History/Changelog
-----------------

1.0.0: 2014-xx-xx
~~~~~~~~~~~~~~~~~

1.0.0 is a huge release. It includes a great deal of changes to ``github3.py``.
It is suggested you read the following release notes *very* carefully.

Breaking Changes
````````````````

- ``Organization#add_member`` has been changed. The second parameter has been
  changed to ``team_id`` and now expects an integer.

- ``Organization#add_repository`` has been changed. The second parameter has been
  changed to ``team_id`` and now expects an integer.

- All methods and functions starting with ``iter_`` have been renamed.

==========================================    ==============================================
Old name                                      New name
==========================================    ==============================================
``github3.iter_all_repos``                    ``github3.all_repositories``
``github3.iter_all_users``                    ``github3.all_users``
``github3.iter_events``                       ``github3.all_events``
``github3.iter_followers``                    ``github3.followers_of``
``github3.iter_following``                    ``github3.followed_by``
``github3.iter_repo_issues``                  ``github3.repository_issues``
``github3.iter_orgs``                         ``github3.organizations_with``
``github3.iter_user_repos``                   ``github3.repositories_by``
``github3.iter_starred``                      ``github3.starred_by``
``github3.iter_subscriptions``                ``github3.subscriptions_for``
``Gist#iter_comments``                        ``Gist#comments``
``Gist#iter_commits``                         ``Gist#commits``
``Gist#iter_files``                           ``Gist#files``
``Gist#iter_forks``                           ``Gist#forks``
``GitHub#iter_all_repos``                     ``GitHub#all_repositories``
``GitHub#iter_all_users``                     ``GitHub#all_users``
``GitHub#iter_authorizations``                ``GitHub#authorizations``
``GitHub#iter_emails``                        ``GitHub#emails``
``GitHub#iter_events``                        ``GitHub#events``
``GitHub#iter_followers``                     ``GitHub#{followers,followers_of}``
``GitHub#iter_following``                     ``GitHub#{following,followed_by}``
``GitHub#iter_gists``                         ``GitHub#{gists,gists_by,public_gists}``
``GitHub#iter_notifications``                 ``GitHub#notifications``
``GitHub#iter_org_issues``                    ``GitHub#organization_issues``
``GitHub#iter_issues``                        ``GitHub#issues``
``GitHub#iter_user_issues``                   ``GitHub#user_issues``
``GitHub#iter_repo_issues``                   ``GitHub#repository_issues``
``GitHub#iter_keys``                          ``GitHub#keys``
``GitHub#iter_orgs``                          ``GitHub#{organizations,organizations_with}``
``GitHub#iter_repos``                         ``GitHub#reposistories``
``GitHub#iter_user_repos``                    ``GitHub#repositories_by``
``GitHub#iter_user_teams``                    ``GitHub#user_teams``
``Organization#iter_members``                 ``Organization#members``
``Organization#iter_public_members``          ``Organization#public_members``
``Organization#iter_repos``                   ``Organization#repositories``
``Organization#iter_teams``                   ``Organization#teams``
``PullRequest#iter_comments``                 ``PullRequest#review_comments``
``PullRequest#iter_commits``                  ``PullRequest#commits``
``PullRequest#iter_files``                    ``PullRequest#files``
``PullRequest#iter_issue_comments``           ``PullRequest#issue_comments``
``Team#iter_members``                         ``Team#members``
``Team#iter_repos``                           ``Team#repositories``
``Repository#iter_assignees``                 ``Repository#assignees``
``Repository#iter_branches``                  ``Repository#branches``
``Repository#iter_code_frequency``            ``Repository#code_frequency``
``Repository#iter_collaborators``             ``Repository#collaborators``
``Repository#iter_comments``                  ``Repository#comments``
``Repository#iter_comments_on_commit``        ``Repository#comments_on_commit``
``Repository#iter_commit_activity``           ``Repository#commit_activity``
``Repository#iter_commits``                   ``Repository#commits``
``Repository#iter_contributor_statistics``    ``Repository#contributor_statistics``
``Repository#iter_contributors``              ``Repository#contributors``
``Repository#iter_forks``                     ``Repository#forks``
``Repository#iter_hooks``                     ``Repository#hooks``
``Repository#iter_issues``                    ``Repository#issues``
``Repository#iter_issue_events``              ``Repository#issue_events``
``Repository#iter_keys``                      ``Repository#keys``
``Repository#iter_labels``                    ``Repository#labels``
``Repository#iter_languages``                 ``Repository#languages``
``Repository#iter_milestones``                ``Repository#milestones``
``Repository#iter_network_events``            ``Repository#network_events``
``Repository#iter_notifications``             ``Repository#notifications``
``Repository#iter_pages_builds``              ``Repository#pages_builds``
``Repository#iter_pulls``                     ``Repository#pull_requests``
``Repository#iter_refs``                      ``Repository#refs``
``Repository#iter_releases``                  ``Repository#releases``
``Repository#iter_stargazers``                ``Repository#stargazers``
``Repository#iter_subscribers``               ``Repository#subscribers``

==========================================    ==============================================

- ``github3.login`` has been simplified and split into two functions:

  - ``github3.login`` serves the majority use case and only provides an 
    authenticated ``GitHub`` object.

  - ``github3.enterprise_login`` allows GitHub Enterprise users to log into 
    their service.

- ``GitHub#iter_followers`` was split into two functions:

  - ``GitHub#followers_of`` which iterates over all of the followers of a user
    whose username you provide

  - ``GitHub#followers`` which iterates over all of the followers of the
    authenticated user

- ``GitHub#iter_following`` was split into two functions:

  - ``GitHub#followed_by`` which iterates over all of the users followed by
    the username you provide

  - ``GitHub#following`` which iterates over all of the users followed by the
    authenticated user

- ``GitHub#iter_gists`` was split into three functions:

  - ``GitHub#public_gists`` which iterates over all of the public gists on 
    GitHub

  - ``GitHub#gists_for`` which iterates over all the public gists of a 
    specific user

  - ``GitHub#gists`` which iterates over the authenticated users gists

- ``GitHub#iter_orgs`` was split into two functions:

  - ``GitHub#organizations`` which iterates over the authenticated user's
    organization memberships

  - ``GitHub#organizations_with`` which iterates over the given user's
    organization memberships

- ``GitHub#iter_subscriptions`` was split into two functions:

  - ``GitHub#subscriptions_for`` which iterates over an arbitrary user's
    subscriptions

  - ``GitHub#subscriptions`` which iterates over the authenticated user's 
    subscriptions

- ``GitHub#iter_starred`` was split into two functions:

  - ``GitHub#starred_by`` which iterates over an arbitrary user's stars

  - ``GitHub#starred`` which iterates over the authenticated user's stars

- Remove legacy watching API:

  - ``GitHub#subscribe``

  - ``GitHub#unsubscribe``

  - ``GitHub#is_subscribed``

- ``Repository#set_subscription`` was split into two simpler functions

  - ``Repository#subscribe`` subscribes the authenticated user to the 
    repository's notifications

  - ``Repository#ignore`` ignores notifications from the repository for the 
    authenticated user

- ``Organization#add_repo`` and ``Team#add_repo`` have been renamed to
  ``Organization#add_repository`` and ``Team#add_repository`` respectively.

- ``Organization#create_repo`` has been renamed to
  ``Organization#create_repository``. It no longer accepts ``has_downloads``.
  It now accepts ``license_template``.

- ``Organization#remove_repo`` has been renamed to
  ``Organization#remove_repository``. It now accepts ``team_id`` instead of
  ``team``.

- ``github3.ratelimit_remaining`` was removed

- ``GitHub`` instances can no longer be used as context managers

- The pull request API has changed.

  - The ``links`` attribute now contains the raw ``_links`` attribute from the
    API.

  - The ``merge_commit_sha`` attribute has been removed since it was deprecated
    in the GitHub API.

  - To present a more consistent universal API, certain attributes have been
    renamed.

===============================     ==========================
Old name                            New attribute name
===============================     ==========================
``PullFile.additions``              ``additions_count``
``PullFile.deletions``              ``deletions_count``
``PullFile.changes``                ``changes_count``
``PullRequest.additions``           ``additions_count``
``PullRequest.comments``            ``comments_count``
``PullRequest.commits``             ``commits_count``
``PullRequest.deletions``           ``deletions_count``
``PullRequest.review_comments``     ``review_comments_count``
===============================     ==========================

- The Gist API has changed.

  - The ``forks`` and ``files`` attributes that used to keep count of the
    number of ``forks`` and ``files`` have been **removed**.

  - The ``comments`` attribute which provided the number of comments on a
    gist, has been **renamed** to ``comments_count``.

  - The ``is_public`` method has been removed since it just returned the
    ``Gist.public`` attribute.

- Most instances of ``login`` as a parameter have been changed to ``username``
  for clarity and consistency. This affects the following methods:

    - ``Organization#add_member``
    - ``Organization#is_member``
    - ``Organization#is_public_member``
    - ``Organization#remove_member``
    - ``Repository#add_collaborator``
    - ``Repository#is_assignee``
    - ``Repository#is_collaborator``
    - ``Repository#remove_collaborator``
    - ``Team#add_member``
    - ``Team#is_member``

- ``Repository.stargazers`` is now ``Repository.stargazers_count`` (conforming
  with the attribute name returned by the API).

0.9.0: 2014-05-04
~~~~~~~~~~~~~~~~~

- Add Deployments API

- Add Pages API

- Add support so applications can revoke a `single authorization`_ or `all
  authorizations`_ created by the application

- Add the ability for users to ping_ hooks

- Allow users to list a `Repository's collaborators`_

- Allow users to create an empty blob on a Repository

- Update how users can list issues and pull requests. See:
  http://developer.github.com/changes/2014-02-28-issue-and-pull-query-enhancements/
  This includes breaking changes to ``Repository#iter_pulls``.

- Update methods to handle the `pagination changes`_.

- Fix typo `stargarzers_url`_

- Add ``assets`` attribute to ``Release`` object.

- Fix wrong argument to ``Organization#create_team`` (``permissions`` versus 
  ``permission``)

- Fix Issue Search Result's representation and initialization

- Fix Repository Search Result's initialization

- Allow users to pass a two-factor authentication callback to 
  ``GitHub#authorize``.

.. _single authorization: https://github3py.readthedocs.org/en/latest/github.html#github3.github.GitHub.revoke_authorization
.. _all authorizations: https://github3py.readthedocs.org/en/latest/github.html#github3.github.GitHub.revoke_authorizations
.. _ping: https://github3py.readthedocs.org/en/latest/repos.html?highlight=ping#github3.repos.hook.Hook.ping
.. _Repository's collaborators: https://github3py.readthedocs.org/en/latest/repos.html#github3.repos.repo.Repository.iter_collaborators
.. _pagination changes: https://developer.github.com/changes/2014-03-18-paginating-method-changes/
.. _stargarzers_url: https://github.com/sigmavirus24/github3.py/pull/240

0.8.2: 2014-02-11
~~~~~~~~~~~~~~~~~

- Fix bug in ``GitHub#search_users`` (and ``github3.search_users``). Thanks
  @abesto

- Expose the stargazers count for repositories. Thanks @seveas

0.8.1: 2014-01-26
~~~~~~~~~~~~~~~~~

- Add documentation for using Two Factor Authentication

- Fix oversight where ``github3.login`` could not be used for 2FA

0.8.0: 2014-01-03
~~~~~~~~~~~~~~~~~

- **Breaking Change** Remove legacy search API

  I realize this should have been scheduled for 1.0 but I was a bit eager to 
  remove this.

- Use Betamax to start recording integration tests

- Add support for Releases API

- Add support for Feeds API

- Add support for Two-Factor Authentication via the API

- Add support for New Search API

  - Add ``github3.search_code``, ``github3.search_issues``, 
    ``github3.search_repositories``, ``github3.search_users``

  - Add ``GitHub#search_code``, ``GitHub#search_issues``, 
    ``GitHub#search_repositories``, ``GitHub#search_users``

- Switch to requests >= 2.0

- Totally remove all references to the Downloads API

- Fix bug in ``Repository#update_file`` where ``branch`` was not being sent to
  the API. Thanks @tpetr!

- Add ``GitHub#rate_limit`` to return all of the information from the
  ``/rate_limit`` endpoint.

- Catch missing attributes -- ``diff_hunk``, ``original_commit_id`` -- on 
  ``ReviewComment``.

- Add support for the Emojis endpoint

- Note deprecation of a few object attributes

- Add support for the ``ReleaseEvent``

- Add ``GitHub#iter_user_teams`` to return all of the teams the authenticated 
  user belongs to

0.7.1: 2013-09-30
~~~~~~~~~~~~~~~~~

- Add dependency on uritemplate.py_ to add URITemplates to different classes.  
  See the documentation for attributes which are templates.

- Fixed issue trying to parse ``html_url`` on Pull Requests courtesy of 
  @rogerhu.

- Remove ``expecter`` as a test dependency courtesy of @esacteksab.

- Fixed issue #141 trying to find an Event that doesn't exist.

.. _uritemplate.py: https://github.com/sigmavirus24/uritemplate

0.7.0: 2013-05-19
~~~~~~~~~~~~~~~~~

- Fix ``Issue.close``, ``Issue.reopen``, and ``Issue.assign``. (Issue #106)

- Add ``check_authorization`` to the ``GitHub class`` to cover the `new part 
  of the API <http://developer.github.com/v3/oauth/#check-an-authorization>`_.

- Add ``create_file``, ``update_file``, ``delete_file``, 
  ``iter_contributor_statistics``, ``iter_commit_activity``, 
  ``iter_code_frequency`` and ``weekly_commit_count`` to the ``Repository`` 
  object.

- Add ``update`` and ``delete`` methods to the ``Contents`` object.

- Add ``is_following`` to the ``User`` object.

- Add ``head``, ``base`` parameters to ``Repository.iter_pulls``.

- The signature of ``Hook.edit`` has changed since that endpoint has changed 
  as well. See: 
  github/developer.github.com@b95f291a47954154a6a8cd7c2296cdda9b610164

- ``github3.GitHub`` can now be used as a context manager, e.g.,
  ::

       with github.GitHub() as gh:
           u = gh.user('sigmavirus24')

0.6.1: 2013-04-06
~~~~~~~~~~~~~~~~~

- Add equality for labels courtesy of Alejandro Gomez (@alejandrogomez)

0.6.0: 2013-04-05
~~~~~~~~~~~~~~~~~

- Add ``sort`` and ``order`` parameters to ``github3.GitHub.search_users`` and 
  ``github3.GitHub.search_repos``.

- Add ``iter_commits`` to ``github3.gists.Gist`` as a means of re-requesting 
  just the history from GitHub and iterating over it.

- Add minimal logging (e.g., ``logging.getLogger('github3')``)

- Re-organize the library a bit. (Split up repos.py, issues.py, gists.py and a 
  few others into sub-modules for my sanity.)

- Calling ``refresh(True)`` on a ``github3.structs.GitHubIterator`` actually 
  works as expected now.

- API ``iter_`` methods now accept the ``etag`` argument as the
  ``GitHub.iter_`` methods do.

- Make ``github3.octocat`` and ``github3.github.GitHub.octocat`` both support
  sending messages to make the Octocat say things. (Think cowsay)

- Remove vendored dependency of PySO8601.

- Split ``GitHub.iter_repos`` into ``GitHub.iter_user_repos`` and 
  ``GitHub.iter_repos``. As a consequence ``github3.iter_repos`` is now 
  ``github3.iter_user_repos``

- ``IssueComment.update`` was corrected to match GitHub's documentation

- ``github3.login`` now accepts an optional ``url`` parameter for users of the 
  ``GitHubEnterprise`` API, courtesy of Kristian Glass (@doismellburning)

- Several classes now allow their instances to be compared with ``==`` and 
  ``!=``. In most cases this will check the unique id provided by GitHub. In 
  others, it will check SHAs and any other guaranteed immutable and unique 
  attribute. The class doc-strings all have information about this and details 
  about how equivalence is determined.

0.5.3: 2013-03-19
~~~~~~~~~~~~~~~~~

- Add missing optional parameter to Repository.contents. Thanks @tpetr

0.5.2: 2013-03-02
~~~~~~~~~~~~~~~~~

- Stop trying to decode the byte strings returned by ``b64decode``. Fixes #72

0.5.1: 2013-02-21
~~~~~~~~~~~~~~~~~

- Hot fix an issue when a user doesn't have a real name set

0.5: 2013-02-16
~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~

- Add API for GitHub Enterprise customers.

0.1b2: 2012-11-10
~~~~~~~~~~~~~~~~~

- Handle 500 errors better, courtesy of Kristian Glass (@doismellburning)
- Handle sending json with `%` symbols better, courtesy of Kristian Glass
- Correctly handle non-GitHub committers and authors courtesy of Paul Swartz 
  (@paulswartz)
- Correctly display method signatures in documentation courtesy of (@seveas)

0.1b1: 2012-10-31
~~~~~~~~~~~~~~~~~

- unit tests implemented using mock instead of hitting the GitHub API (#37)
- removed ``list_*`` functions from GitHub object
- Notifications API coverage

0.1b0: 2012-10-06
~~~~~~~~~~~~~~~~~

- Support for the complete GitHub API (accomplished)

  - Now also includes the Statuses API
  - Also covers the auto_init parameters to the Repository creation 
    methodology
  - Limited implementation of iterators in the place of list functions.

- 98% coverage by unit tests
