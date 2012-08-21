#!/usr/bin/env python
# Originally co-authored by Jeff V Stein and Ian Cordasco for Todo.txt-python
# (http://git.io/todo.py)

import unittest
import sys
import os
import re
from getpass import getpass

try:
    import readline
    readline.parse_and_bind('tab: complete')
except ImportError:
    pass

if __name__ == "__main__":
    if not (os.environ.get('CI') or os.environ.get('TRAVIS')):
        if hasattr(__builtins__, 'raw_input'):
            prompt = raw_input
        else:
            prompt = input
        user = pw = ''
        while not user:
            user = prompt('Enter GitHub username: ')
        while not pw:
            pw = getpass('Password for {0}: '.format(user))

        os.environ['__USER'] = user
        os.environ['__PASS'] = pw

    if sys.version_info >= (2, 7):
        suite = unittest.defaultTestLoader.discover("tests")
    else:
        names = os.listdir("tests")
        regex = re.compile("(?!_+)\w+\.py$")
        join = '.'.join
        names = [join(['tests', f[:-3]]) for f in names if regex.match(f)]
        suite = unittest.defaultTestLoader.loadTestsFromNames(names)

    print("=== Starting unittest suite ===")
    unittest.TextTestRunner(verbosity=1).run(suite)
