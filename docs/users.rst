.. module:: github3
.. module:: github3.users

User
====

This part of the documentation covers:

- :class:`User <User>`
- :class:`Key <Key>`
- :class:`Plan <Plan>`

None of these objects should ever be instantiated by the user (developer).

**When listing users, GitHub only sends a handful of the object's attributes.  
To retrieve all of the object's attributes, you must call the refresh() 
method. This unfortunately requires another call to the API, so use it 
sparingly if you have a low limit**

User Modules
------------

.. autoclass:: User
    :inherited-members:

------

.. autoclass:: Key
    :inherited-members:

------

.. autoclass:: Plan
    :inherited-members:
