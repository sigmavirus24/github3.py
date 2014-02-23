Events
======

.. module:: github3
.. module:: github3.events

This part of the documentation covers the :class:`Event <Event>` object.

Event Objects
-------------

.. autoclass:: Event
    :inherited-members:

When accessing the payload of the event, you should notice that you receive a
dictionary where the keys depend on the event type_. Note:

- where they reference an array in the documentation but index it like a
  dictionary, you are given a regular dictionary
- where they reference a key as returning an object, you receive the equivalent
  object from the dictionary, e.g., for a Fork Event::

        >>> event
        <Event [Fork]>
        >>> event.payload
        {u'forkee': <Repository [eweap/redactor-js]>}
        >>> event.payload['forkee']
        <Repository [eweap/redactor-js]>

Using the dictionary returned as the payload makes far more sense than creating
an object for the payload in this instance. For one, creating a class for each
payload type would be insanity. I did it once, but it isn't worth the effort.
Having individual handlers as we have now which modify the payload to use our
objects when available is more sensible.

.. links
.. _type: http://developer.github.com/v3/events/types
