Using Two-factor Authentication with github3.py
===============================================

GitHub recently added support for Two-factor Authentication to ``github.com``
and shortly thereafter added support for it on ``api.github.com``. In version
0.8, github3.py also added support for it and you can use it right now.

To use Two-factor Authentication, you must define your own function that will
return your one time authentication code. You then provide that function when
logging in with github3.py.

For example:

.. code::

    import github3

    def my_two_factor_function():
        # The user could accidentally press Enter before being ready,
        # let's protect them from doing that.
        return input('Enter 2FA code: ').strip() or my_two_factor_function()

    g = github3.login('sigmavirus24', 'my_password',
                      two_factor_callback=my_two_factor_function)

Then each time the API tells github3.py it requires a Two-factor Authentication
code, github3.py will call ``my_two_factor_function`` which prompt you for it.
