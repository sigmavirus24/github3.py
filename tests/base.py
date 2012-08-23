import os
import sys
import unittest
import github3
from expecter import expect, add_expectation


class BaseTest(unittest.TestCase):
    api = 'https://api.github.com/'
    kr = 'kennethreitz'
    sigm = 'sigmavirus24'
    todo = 'Todo.txt-python'
    gh3py = 'github3py'
    test_repo = 'github3.py_test'

    def setUp(self):
        super(BaseTest, self).setUp()
        self.g = github3.GitHub()
        self.auth = False
        user = self.user = os.environ.get('__USER')
        pw = os.environ.get('__PASS')
        if user and pw:
            self._g = github3.login(user, pw)
            self.auth = True

    def assertIsNotNone(self, value, msg=None):
        if sys.version_info >= (2, 7):
            super(BaseTest, self).assertIsNotNone(value, msg)
        else:
            try:
                assert value is not None
            except AssertionError:
                self.fail(msg)

    def assertAreNotNone(self, obj, *attrs):
        """Assert the attributes of the object are not none"""
        for attr in attrs:
            self.assertIsNotNone(getattr(obj, attr),
                '{0} is None'.format(attr))

    def expect_list_of_class(self, l, cls):
        for i in l:
            expect(i).isinstance(cls)


def is_not_None(var):
    return var is not None


def is_None(var):
    return var is None


def is_True(var):
    return var is True


def is_False(var):
    return var is False

add_expectation(is_not_None)
add_expectation(is_None)
add_expectation(is_True)
add_expectation(is_False)

if sys.version_info >= (3, 0):
    str_test = (str, bytes)
else:
    str_test = (str, unicode)
