TODO
====

High priority
-------------

(In order of priority)

unittests
~~~~~~~~~

- We're currently at ~85% coverage. I want to get each module close to if not 
  above 90% coverage before December. 100% by next year (at the latest).
- Develop/find a better way to run the tests. Since I'm doing as much testing 
  directly against the API as possible, running the tests takes a while and 
  we're only at 85% coverage.

remove ``@property`` decorated functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- I hadn't considered that because these were functions, they add unnecessary 
  delay in accessing the attributes. If someone is insistent on presenting bad 
  information to an end-user, they'll do it no matter what, so I may as well 
  just make maintaining the code easier on myself.

plan
++++

- Wherever there is a ``@property`` decorated function that just returns a 
  value, rename that value to the name of the function everywhere in the 
  class.

pagination
~~~~~~~~~~

- Certain calls should accept a way of doing pagination. There are comments 
  around those calls

github3.api
~~~~~~~~~~~

- Add anonymous functionality for more areas of the API

Low priority
------------

(In order of priority)

Plan
====

- Finish unittests
- Brainstorm ideas on how to give access to paginated functions, e.g., 
  ``Repository.list_issues()``.

  Initial problems with pagination:

  * Where to store the relative links for each request.

    Ideas:

    - Each function generates a URL for each call which is technically unique.  
      We could have a global dictionary which uses the generated URL as a key 
      and stores the relative links. Each time the call for pagination 
      happens, e.g.,

      ::
        
        repo.list_issues(rel_link='next')

      We replace the old set of relative links with the new set.

  * How to have the user invoke the next link.

    Ideas:

    - Add one more parameter to the function (or decorator if using above 
      idea) that accepts the argument: ``rel_link``. If the call was not 
      previously made, just return the first list of objects. We will not ever 
      try to guess what the user wants, so this will be the standard behavior.

  What is already done for pagination:

  * Requests now has link parsing built into it.
