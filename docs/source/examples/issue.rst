Issue Code Examples
===================

Examples using ``Issue``\ s

Administering Issues
--------------------

Let's assume you have your username and password stored in ``user`` and ``pw``
respectively, you have your repository name stored in ``repo``, and the number
of the issue you're concerned with in ``num``.

::

    from github3 import login

    gh = login(user, pw)
    issue = gh.issue(user, repo, num)
    if issue.is_closed():
        issue.reopen()

    issue.edit('New issue title', issue.body + '\n------\n**Update:** Text to append')

Closing and Commenting on Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Assuming issue is the same as above ...
    issue.create_comment('This should be fixed in 6d4oe5. Closing as fixed.')
    issue.close()

Example issue to comment on
---------------------------

If you would like to test the above, see
`issue #108 <https://github.com/sigmavirus24/github3.py/issues/108>`_. Just
follow the code there and fill in your username, password (or token), and
comment message. Then run the script and watch as the issue opens in your
browser focusing on the comment **you** just created.

The following shows how you could use github3.py to fetch and display your
issues in your own style and in your web browser.

.. literalinclude:: source/browser.py
    :language: python

Or how to do the same by wrapping the lines in your terminal.

.. literalinclude:: source/wrap_text.py
    :language: python

Importing an issue
------------------

Not only can you create new issues, but you can import existing ones.  When
importing, you preserve the timestamp creation date; you can preserve the
timestamp(s) for comment(s) too.

::

   import github3
   gh = github3.login(token=token)
   issue = {
      'title': 'Documentation issue',
      'body': 'Missing links in index.html',
      'created_at': '2011-03-11T17:00:40Z'
   }

   repository = gh.repository(user, repo)
   repository.import_issue(**issue)

Status of imported issue
~~~~~~~~~~~~~~~~~~~~~~~~

Here's how to check the status of the imported issue.

::

    import github3
    issue = repository.imported_issue(issue_num)
    print issue.status
