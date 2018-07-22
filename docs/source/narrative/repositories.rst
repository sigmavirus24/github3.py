===========================
 Using the Repository APIs
===========================

Now that we have :doc:`learned <getting-started>` how to set up a client for
use with our APIs, let's begin to review how github3.py implements the
`Repositories API`_.


Retrieving Repositories
=======================

Once you've :ref:`logged in <logging-in>` you will have an instance of
:class:`~github3.github.GitHub` or :class:`~github3.github.GitHubEnterprise`.
Let's assume either one is bound to a variable called ``github``. To retrieve
a single :class:`repository <github3.repos.repo.Repository>` that we know the
owner and name of, we would do the following:

.. code-block:: python

    repository = github.repository(owner, repository_name)

For example, let's retrieve the repository of the ``uritemplate`` package that
github3.py relies on:

.. code-block:: python

    uritemplate = github.repository('python-hyper', 'uritemplate')

It's also possible for us to retrieve multiple repositories owned by the same
user or organization:

.. code-block:: python

    for short_repository in github.repositories_by('python-hyper'):
        ...

When listing repositories, like listing other objects, the GitHub API doesn't
return the full representation of the object. In this case, github3.py returns
a different object to represent a :class:`short repository
<github3.repos.repo.ShortRepository>`. This object has fewer attributes, but
can be converted into a full repository like so:

.. code-block:: python

    for short_repository in github.repositories_by('python-hyper'):
        full_repository = short_repository.refresh()

We now have two separate objects for the repository based on how GitHub
represents them. Both objects have the same methods attached to them. There's
just a different set of attributes on each.


Interacting with Repositories
=============================

Repositories are central to many things in GitHub as well as in the API and as
result they have many attributes and methods. It's possible to list branches,
collaborators, commits, contributors, deployments, forks, issues, projects,
pull requests, refs, and more.

For example, we could build a tiny function that checks if a contributor has
deleted their fork:

.. code-block:: python

    uritemplate = github.repository('python-hyper', 'uritemplate')
    contributors_without_forks = (set(uritemplate.contributors()) -
                                  set(fork.owner for fork in uritemplate.forks()))
    print(f'The following contributors deleted their forks of {uritemplate!r}')
    for contributor in sorted(contributors_without_forks, key=lambda c: c.login):
        print(f'  * {contributor.login}')

The output should look like

.. code-block:: text

    The following contributors deleted their forks of <Repository [python-hyper/uritemplate]>
      * eugene-eeo
      * jpotts18
      * sigmavirus24
      * thierryba



.. links
.. _Repositories API:
    https://github.com/sigmavirus24/github3.py/pull/836
