#!/usr/bin/env python
# Originally co-authored by Jeff V Stein and Ian Cordasco for Todo.txt-python 
# (http://git.io/todo.py)

import unittest
import sys
import os
import re
import tests

if __name__ == "__main__":
    if sys.version_info >= (2, 7):
        suite = unittest.defaultTestLoader.discover("tests")
    else:
        names = os.listdir("tests")
        regex = re.compile("(?!_+)\w+\.py$")
        join = '.'.join
        names = [join(['tests', f[:-3]]) for f in names if regex.match(f)]
        print(names)
        suite = unittest.defaultTestLoader.loadTestsFromNames(names)

    print("=== Starting unittest suite ===")
    unittest.TextTestRunner(verbosity=2).run(suite)
