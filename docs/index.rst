github3.py
==========

Release v\ |version|.

github3.py is wrapper for the `GitHub API`_ written in python. The design of
github3.py is centered around having a logical organization of the methods
needed to interact with the API. Let me demonstrate this with a code example.

Example
-------

Let's get information about a user::

    from github3 import login

    gh = login('sigmavirus24', password='<password>')

    sigmavirus24 = gh.user()
    # <User [sigmavirus24:Ian Cordasco]>

    print(sigmavirus24.name)
    # Ian Cordasco
    print(sigmavirus24.login)
    # sigmavirus24
    print(sigmavirus24.followers)
    # 4

    for f in gh.iter_followers():
        print(str(f))

    kennethreitz = gh.user('kennethreitz')
    # <User [kennethreitz:Kenneth Reitz]>

    print(kennethreitz.name)
    print(kennethreitz.login)
    print(kennethreitz.followers)

    followers = [str(f) for f in gh.iter_followers('kennethreitz')]

More Examples
~~~~~~~~~~~~~

.. toctree::
    :maxdepth: 2

    examples/two_factor_auth
    examples/oauth
    examples/gist
    examples/git
    examples/github
    examples/issue
    examples/iterators.rst
    examples/logging
    examples/octocat


.. links

.. _GitHub API: http://developer.github.com


Modules
-------

.. toctree::
    :maxdepth: 1

    api
    auths
    events
    gists
    git
    github
    issues
    models
    notifications
    orgs
    pulls
    repos
    search_structs
    structs
    users

Internals
~~~~~~~~~

For objects you're not likely to see in practice. This is useful if you ever
feel the need to contribute to the project.

.. toctree::
    :maxdepth: 1

    models
    decorators


Installation
------------

.. code-block:: sh

    $ pip install github3.py
    # OR:
    $ git clone git://github.com/sigmavirus24/github3.py.git github3.py
    $ cd github3.py
    $ python setup.py install


Dependencies
~~~~~~~~~~~~

- requests_ by Kenneth Reitz
- uritemplate.py_ by Ian Cordasco

.. _requests: https://github.com/kennethreitz/requests
.. _uritemplate.py: https://github.com/sigmavirus24/uritemplate


Contributing
------------

I'm maintaining two public copies of the project. The first can be found on 
GitHub_ and the second on BitBucket_. I would prefer pull requests to take 
place on GitHub, but feel free to do them via BitBucket. Please make sure to 
add yourself to the list of contributors in AUTHORS.rst, especially if you're 
going to be working on the list below.

.. links
.. _GitHub: https://github.com/sigmavirus24/github3.py
.. _BitBucket: https://bitbucket.org/icordasc/github3.py/src

Contributor Friendly Work
~~~~~~~~~~~~~~~~~~~~~~~~~

In order of importance:

Documentation

    I know I'm not the best at writing documentation so if you want to clarify 
    or correct something, please do so.

Examples

    Have a clever example that takes advantage of github3.py? Feel free to 
    share it.

Running the Unittests
~~~~~~~~~~~~~~~~~~~~~

::

    mkdir -p /path/to/virtualenv/github3.py
    cd /path/to/virtualenv/github3.py
    virtualenv .
    cd /path/to/github3.py_repo/
    pip install -r dev-requirements.txt
    # Or you could run make test-deps
    make tests


.. toctree::

    testing


Contact
-------

- Twitter: @\ sigmavirus24_
- Private email: graffatcolmingov [at] gmail
- Mailing list: github3.py [at] librelist.com

.. _sigmavirus24: https://twitter.com/sigmavirus24

.. include:: ../HISTORY.rst

Testimonials
------------

.. raw:: html

    <blockquote class="twitter-tweet"><p>gotta hand it to @<a 
    href="https://twitter.com/sigmavirus24">sigmavirus24</a> ... github3.py is 
    really well written. It will soon be powering the github stuff on
    @<a href="https://twitter.com/workforpie">workforpie</a>
    </p>&mdash; Brad Montgomery # (@bkmontgomery) <a 
    href="https://twitter.com/bkmontgomery/status/325644863561400320">April 20, 2013</a>
    </blockquote>

    <blockquote class="twitter-tweet"><p>awesome github v3 api wrapper in 
    python <a href="https://t.co/PhD0Aj5X" 
    title="https://github.com/sigmavirus24/github3.py">github.com/sigmavirus24/g#</a></p>&mdash; 
    Mahdi Yusuf (@myusuf3) <a 
    href="https://twitter.com/myusuf3/status/258571050927915008">October 17, 
    2012</a></blockquote>

    <blockquote class="twitter-tweet">
    <p>@<a href="https://twitter.com/sigmavirus24">sigmavirus24</a> github3 is 
    awesome! Made my life much easier tonight, which is a very good 
    thing.</p>&mdash; Mike Grouchy (@mgrouchy) <a 
    href="https://twitter.com/mgrouchy/status/316370772782350336">March 26, 
    2013</a></blockquote>

    <blockquote class="twitter-tweet" data-conversation="none">
    <p>@<a href="https://twitter.com/sigmavirus24">sigmavirus24</a> "There are 
    so many Python client libraries for GitHub API, I tried all of them, and 
    my conclusion is: github3.py is the best."</p>&mdash; Hong Minhee 
    (@hongminhee) <a 
    href="https://twitter.com/hongminhee/status/315295733899210752">March 23, 
    2013</a></blockquote>

    <blockquote class="twitter-tweet">
    <p>@<a href="https://twitter.com/sigmavirus24">sigmavirus24</a> I cannot 
    wait to use your github package for <a 
    href="https://twitter.com/search/%23zci">#zci</a>. Do you have it packaged 
    for debian by any chance?</p>&mdash; Zygmunt Krynicki (@zygoon) <a 
    href="https://twitter.com/zygoon/status/316608301527887872">March 26, 
    2013</a></blockquote>

    <blockquote class="twitter-tweet">
    <p>Developing against github3.py's API is a joy, kudos to @<a 
    href="https://twitter.com/sigmavirus24">sigmavirus24</a></p>&mdash; 
    Alejandro Gomez (@dialelo) <a 
    href="https://twitter.com/dialelo/status/316846075015229440">March 27, 
    2013</a></blockquote>

    <script async src="//platform.twitter.com/widgets.js" 
    charset="utf-8"></script>
