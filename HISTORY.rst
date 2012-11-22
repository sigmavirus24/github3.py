History/Changelog
=================

0.2: 2012-11-21
---------------

MAJOR API CHANGES:

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
- Correctly display method signatures in documentatio

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
