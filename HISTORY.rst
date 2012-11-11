History/Changelog
=================

0.1: 2012-xx-xx
---------------

- 100% unit test coverage

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
