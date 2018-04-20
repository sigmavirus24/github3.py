.. _loggingex:

Using Logging with github3.py
=============================

.. versionadded:: 0.6.0

The following example shows how to set up logging for github3.py. It is off by
default in the library and will not pollute your logs.

.. literalinclude:: source/logging_ex.py
    :language: python

One thing to note is that if you want more detailed information about what is
happening while the requests are sent, you can do the following:

.. code-block:: python

    import logging
    urllib3 = logging.getLogger('requests.packages.urllib3')

And configure the logger for urllib3. Unfortunately, requests itself doesn't
provide any logging, so the best you can actually get is by configuring
``urllib3``.

You will see messages about the following in the logs:

* Construction of URLs used in requests, usually in the form:
  ``('https://api.github.com', 'repos', 'sigmavirus24', 'github3.py')``
* What request is being sent, e.g.,
  ``POST https://api.github.com/user kwargs={}``
* If JSON is trying to be extracted from the response, what the response's
  status code was, what the expected status code was and whether any JSON was
  actually returned.
