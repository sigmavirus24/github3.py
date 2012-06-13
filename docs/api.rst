.. _api:

===
API
===

.. module:: github3

API documentation

Main Interface
==============

To interact with the GitHub API you can either authenticate to access protected
functionality or you can interact with it anonymously.

To authenticate, you simply use ``login()``.

.. autofunction:: login

To use the API anonymously, you simply create a new GitHub object.
