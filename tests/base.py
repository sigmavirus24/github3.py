import os
import sys
import unittest
import github3
import expecter


class BaseTest(unittest.TestCase):
    api = 'https://api.github.com/'
    kr = 'kennethreitz'
    sigm = 'sigmavirus24'
    todo = 'Todo.txt-python'
    gh3py = 'github3py'
    test_repo = 'github3.py_test'

    def __init__(self, methodName='runTest'):
        super(BaseTest, self).__init__(methodName)
        self.auth = False
        user = self.user = os.environ.get('__USER')
        pw = self.pw = os.environ.get('__PASS')
        self.g = github3.GitHub()
        if user and pw:
            self._g = github3.login(self.user, self.pw)
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

    def raisesGHE(self, func, *args, **kwargs):
        """Assert that the function, when called, raises a GitHubError."""
        with expect.raises(github3.GitHubError):
            func(*args, **kwargs)

    def expect_list_of_class(self, l, cls):
        for i in l:
            expect(i).isinstance(cls)


class CustomExpecter(expecter.expect):
    def is_not_None(self):
        assert self._actual is not None, (
                'Expected anything but None but got it.'
                )

    def is_None(self):
        assert self._actual is None, (
                'Expected None but got %s' % repr(self._actual)
                )

    def is_True(self):
        assert self._actual is True, (
                'Expected True but got %s' % repr(self._actual)
                )

    def is_False(self):
        assert self._actual is False, (
                'Expected False but got %s' % repr(self._actual)
                )

    def list_of(self, cls):
        expected = cls.__name__
        for actual in self._actual:
            actual_cls = actual.__class__.__name__
            assert isinstance(actual, cls), (
                    'Expected instance of %s but got %s' % (expected,
                        actual_cls)
                    )

expect = CustomExpecter


if sys.version_info >= (3, 0):
    str_test = (str, bytes)
else:
    str_test = (str, unicode)


def expect_str(val):
    expect(val).isinstance(str_test)
    expect(val) != ''
