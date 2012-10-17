#!/usr/bin/env python

import unittest
import os
import re
import coverage


TEST_DIR = 'tests'

if __name__ == "__main__":
    cov = coverage.coverage(source=['github3', 'tests'])
    cov.start()

    # list files in directory tests/
    names = os.listdir(TEST_DIR)
    regex = re.compile("(?!_+)\w+\.py$")
    join = '.'.join
    # Make a list of the names like 'tests.test_name'
    names = [join([TEST_DIR, f[:-3]]) for f in names if regex.match(f)]
    suite = unittest.defaultTestLoader.loadTestsFromNames(names)
    unittest.TextTestRunner(verbosity=1).run(suite)

    cov.stop()
    cov.save()
