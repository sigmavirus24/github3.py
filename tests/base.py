#import os
import sys
import unittest
#from getpass import getpass

#sys.path.insert(0, os.path.abspath('..'))
import github3

class BaseTest(unittest.TestCase):
    api = 'https://api.github.com/'
    kr = 'kennethreitz'
    sigm = 'sigmavirus24'
    todo = 'Todo.txt-python'
    gh3py = 'github3py'

    def setUp(self):
        super(BaseTest, self).setUp()
        self.g = github3.GitHub()
        self.auth = False
        #if not (os.environ.get('CI') or os.environ.get('TRAVIS')):
        #    if hasattr(__builtins__, 'raw_input'):
        #        prompt = raw_input
        #    else:
        #        prompt = input
        #    user = ''
        #    pw = ''
        #    while not user:
        #        user = prompt('Enter GitHub username: ')
        #    while not pw:
        #        pw = getpass('Password for {0}: '.format(user))
        #    self._g = github3.login(user, pw)
        #    self.auth = True

    def assertIsInstance(self, obj, cls):
        """Assert that ``obj`` is an instance of ``cls``"""
        if not isinstance(obj, cls):
            self.fail()

    def assertIsNotNone(self, value, msg=None):
        if sys.version_info >= (2, 7):
            super(BaseTest, self).assertIsNotNone(value, msg)
        else:
            try:
                assert value is not None
            except AssertionError:
                self.fail('AssertionError: ' + msg)
