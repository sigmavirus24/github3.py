import sys
import os
import unittest

#sys.path.insert(0, os.path.abspath('..'))
import github3

class BaseTest(unittest.TestCase):
    api = 'https://api.github.com/'
    def assertIsInstance(self, obj, cls):
        """Assert that ``obj`` is an instance of ``cls``"""
        if not isinstance(obj, cls):
            self.fail()

    def assertRaisesError(self, func, *args, **kwargs):
        """Assert that func raises github3.Error"""
        try:
            func(*args, **kwargs)
        except github3.Error:
            pass
        except Exception, e:
            self.fail('{0}({1}, {2}) raises unexpected exception: {3}'.format(
                str(func), str(args), str(kwargs), str(e)))

    def assertIsNotNone(self, value, msg=None):
        if sys.version_info >= (2, 7):
            super(BaseTest, self).assertIsNotNone(value, msg)
        else:
            try:
                assert value is not None
            except AssertionError:
                self.fail('AssertionError: ' + msg)
