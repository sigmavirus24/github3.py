from github3 import validation
from tests.utils import TestCase


class TestIntegerValidator(TestCase):
    def setUp(self):
        self.v = validation.IntegerValidator()

    def test_is_valid_raises_TypeError(self):
        self.assertRaises(TypeError, self.v.is_valid, None)

    def test_handles_ValueError(self):
        self.assertFalse(self.v.is_valid('abc'))

    def test_accepts_strings_of_digits(self):
        self.assertTrue(self.v.is_valid('123'))

    def test_accepts_integers(self):
        self.assertTrue(self.v.is_valid(123))

    def test_converts_strings_of_digits(self):
        self.assertEqual(123, self.v.convert('123'))

    def test_converts_integers(self):
        self.assertEqual(123, self.v.convert(123))

    def test_convert_raises_TypeError(self):
        self.assertRaises(TypeError, self.v.convert, None)

    def test_allows_none_with_allow_none_True(self):
        self.v.allow_none = True
        self.assertTrue(self.v.is_valid(None))


class TestListValidator(TestCase):
    def setUp(self):
        self.v = validation.ListValidator(
            sub_schema=validation.IntegerValidator()
        )

    def test_is_valid_None(self):
        self.assertFalse(self.v.is_valid(None))
        self.v.allow_none = True
        self.assertTrue(self.v.is_valid(None))

    def test_is_valid_empty_list(self):
        self.assertTrue(self.v.is_valid([]))

    def test_is_valid_list_of_strings(self):
        self.assertFalse(
            self.v.is_valid(
                ["abc", "def"]
            )
        )
