====================
 Events API Classes
====================

This part of the documentation covers the objects that represent data returned
by the Events API.


The Event Object
================

.. autoclass:: github3.events.Event
    :inherited-members:

When accessing the payload of the event, you should notice that you receive a
dictionary where the keys depend on the event type_. Note:

- where they reference an array in the documentation but index it like a
  dictionary, you are given a regular dictionary

- where they reference a key as returning an object, you receive the equivalent
  object from the dictionary, e.g., for a Fork Event

  .. code-block:: python

        >>> event
        <Event [Fork]>
        >>> event.payload
        {u'forkee': <Repository [eweap/redactor-js]>}
        >>> event.payload['forkee']
        <ShortRepository [eweap/redactor-js]>

Using the dictionary returned as the payload makes far more sense than creating
an object for the payload in this instance. For one, creating a class for each
payload type would be insanity. I did it once, but it isn't worth the effort.
Having individual handlers as we have now which modify the payload to use our
objects when available is more sensible.


Event Related Objects
=====================

The following objects are returned as part of an
:class:`~github3.events.Event`. These objects all have methods to convert them
to full representations of the object. For example,
:class:`~github3.events.EventUser` has
:meth:`~github3.events.EventUser.to_user` and aliases
:meth:`~github3.events.EventUser.refresh` to behave similarly.

.. autoclass:: github3.events.EventUser

.. autoclass:: github3.events.EventOrganization

.. autoclass:: github3.events.EventPullRequest

.. autoclass:: github3.events.EventReviewComment

.. autoclass:: github3.events.EventIssue

.. autoclass:: github3.events.EventIssueComment

.. links
.. _type: https://developer.github.com/v3/activity/events/types
