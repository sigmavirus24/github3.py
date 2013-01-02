TODO
====

High priority
-------------

(In order of priority)

requests 1.x
~~~~~~~~~~~~

Upgrade to requests 1.x

unittests
~~~~~~~~~

Rewrite all unittests with mock.

github3.api
~~~~~~~~~~~

- Add anonymous functionality for more areas of the API

github3.*
~~~~~~~~~

- Add sensible defaults to all attributes instead of just using None, e.g.,
  if the user is expecting a string but there is no data to provide, return 
  ``''``.

Low priority
------------

(In order of priority)

logging -- Planned
~~~~~~~~~~~~~~~~~~

I need to determine if there is a desire for logging and where it would be 
most useful. I would probably take a cue from urllib3 in this instance.
