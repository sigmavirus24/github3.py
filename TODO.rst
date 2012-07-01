TODO
====

HIGH PRIORITY
-------------

- Fix installing github3.py when requests doesn't exist on the system already.
  Currently, this fails which prevents pip from installing github3.py. I 
  wonder if no one ran into this problem or if they just didn't bother 
  reporting it.

everywhere
----------

- Use requests ``params`` parameter to send parameters from the URl

github3.api
-----------

- Add anonymous functionality for more areas of the API

unittests
---------

- We need to test everything right now. **EVERYTHING**

Plan
====

- Write unittests for everything possible, try to find as many corner cases as 
  possible
