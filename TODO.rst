TODO
====

High priority
-------------

(In order of priority)

unittests
~~~~~~~~~

- We need to test everything right now. **EVERYTHING**

github3.api
~~~~~~~~~~~

- Add anonymous functionality for more areas of the API

Low priority
------------

(In order of priority)

Slumber
~~~~~~~

- Open a branch to experiment with slumber_ instead of requests. (It will 
  still rely on requests, but slumber just looks so much cleaner that what I 
  have now)

.. links
.. _slumber: http://slumber.in/

Plan
====

- Write unittests for everything possible, try to find as many corner cases as 
  possible
- Brainstorm ideas on how to give access to paginated functions, e.g., 
  ``Repository.list_issues()``.

  Initial problems with pagination:

  * Where to store the relative links for each request.

    Ideas:

    - New decorator which keeps track of the function, the parameters, and the 
      dictionary for the relative links -- might require that the functions on 
      the objects (as they are now) return ``([list of objects], 
      request_object)`` while the decorator receives this, returns to the user 
      the list of objects and processes the ``request_object`` behind the 
      scenes.

  * How to have the user invoke the next link.

    Ideas:

    - Add one more parameter to the function (or decorator if using above 
      idea) that accepts the argument: ``rel_link``. If the call was not 
      previously made, just return the first list of objects (or should we try 
      to return the "requested" list of objects, i.e., maybe the user wanted 
      to skip the first page for some reason).

  What is already done for pagination:

  * Regular expression tested on example relative links (by hand) and 
    precompiled in github3.models.GitHubCore._rel_reg so that whatever calls 
    it can do something like::

        links = requests.headers.get('link')
        # '<https://api.github.com/...>; rel="next", <https://api.gith...>; rel="last"'
        links = links.split(', ')
        for rel_link_str in links:
            matches = self._rel_reg.match(rel_link_str)
            matches.groups()  # ('https://api.github.com/...', 'next')
