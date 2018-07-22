Git Code Examples
=================

The GitHub API does not just provide an API to interact with GitHub's
features. A whole section of the API provides a RESTful API to git operations
that one might normally perform at the command-line or via your git client.

Creating a Blob Object
----------------------

One of the really cool (and under used, it seems) parts of the GitHub API
involves the ability to create blob objects.

.. code-block:: python

    from github3 import login
    g = login(username, password)
    repo = g.repository('sigmavirus24', 'Todo.txt-python')
    sha = repo.create_blob('Testing blob creation', 'utf-8')
    sha
    # u'57fad9a39b27e5eb4700f66673ce860b65b93ab8'
    blob = repo.blob(sha)
    blob.content
    # u'VGVzdGluZyBibG9iIGNyZWF0aW9u\n'
    blob.decoded
    # u'Testing blob creation'
    blob.encoding
    # u'base64'

Creating a Tag Object
---------------------

GitHub provides tar files for download via tag objects. You can create one via
``git tag`` or you can use the API.

.. code-block:: python

    from github3 import login
    g = login(username, password)
    repo = g.repository('sigmavirus24', 'github3.py')
    tag = repo.tag('cdba84b4fede2c69cb1ee246b33f49f19475abfa')
    tag
    # <Tag [cdba84b4fede2c69cb1ee246b33f49f19475abfa]>
    tag.object.sha
    # u'24ea44d302c6394a0372dcde8fd8aed899c0034b'
    tag.object.type
    # u'commit'
