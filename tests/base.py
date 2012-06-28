import sys
import os
import unittest

sys.path.insert(0, os.path.abspath('..'))
import github3

class BaseTest(unittest.TestCase):
    api = 'https://api.github.com/'
    def assertIsInstance(self, obj, cls):
        '''Assert that ``obj`` is an instance of ``cls``'''
        if not isinstance(obj, cls):
            self.fail()
