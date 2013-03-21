#!/usr/bin/env python

import unittest
import imp
import os
import re

try:
    import coverage
except ImportError:
    coverage = None

try:
    for m in ('expecter', 'mock'):
        imp.find_module(m)
except ImportError as ie:
    print('Please install the test dependencies as documented in the README')
    raise

TEST_DIR = 'tests'


def collect_tests():
    # list files in directory tests/
    names = os.listdir(TEST_DIR)
    regex = re.compile("(?!_+)\w+\.py$")
    join = '.'.join
    # Make a list of the names like 'tests.test_name'
    names = [join([TEST_DIR, f[:-3]]) for f in names if regex.match(f)]
    return unittest.defaultTestLoader.loadTestsFromNames(names)

if __name__ == "__main__":
    if coverage:
        cov = coverage.coverage(source=['github3'],
                                omit=['github3/packages/*'])
        cov.exclude('\(No coverage\)')
        cov.exclude('def __repr__')
        cov.start()

    suite = collect_tests()
    unittest.TextTestRunner(verbosity=1).run(suite)

    if coverage:
        cov.stop()
        cov.save()
        cov.report(show_missing=False)
