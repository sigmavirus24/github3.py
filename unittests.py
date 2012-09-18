#!/usr/bin/env python
# Originally co-authored by Jeff V Stein and Ian Cordasco for Todo.txt-python
# (http://git.io/todo.py)

import unittest
import os
import re
from getpass import getpass
from multiprocessing import Pool

try:
    import readline
    readline.parse_and_bind('tab: complete')
except ImportError:
    pass


def load_test(test):
    return unittest.defaultTestLoader.loadTestsFromName(test)

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

    pool = Pool(5)

    names = os.listdir("tests")
    regex = re.compile("(?!_+)\w+\.py$")
    join = '.'.join
    names = [join(['tests', f[:-3]]) for f in names if regex.match(f)]
    result = pool.map_async(load_test, names)
    suites = result.get(timeout=(10 * 60))  # 10 minutes
    suite = suites.pop(0)
    for s in suites:
        suite.addTests(s._tests)

    unittest.TextTestRunner(verbosity=1).run(suite)
