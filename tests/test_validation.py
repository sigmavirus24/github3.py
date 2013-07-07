from github3 import validation
from tests.utils import TestCase


class TestIntegerValidator(TestCase):
    def setUp(self):
        self.v = validation.IntegerValidator()

    def test_is_valid_raises_TypeError(self):
        self.assertRaises(TypeError, self.v.is_valid, {})

    def test_handles_None(self):
        self.assertFalse(self.v.is_valid(None))

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

    def test_None_is_valid(self):
        self.assertFalse(self.v.is_valid(None))
        self.v.allow_none = True
        self.assertTrue(self.v.is_valid(None))

    def test_converts_None(self):
        self.v.allow_none = True
        self.assertEqual(self.v.convert(None), None)

    def test_empty_list_is_valid(self):
        self.assertTrue(self.v.is_valid([]))

    def test_list_of_strings_is_not_valid(self):
        self.assertFalse(self.v.is_valid(["abc", "def"]))

    def test_tuple_of_strings_is_not_valid(self):
        self.assertFalse(self.v.is_valid(("abc", "def")))

    def test_list_of_integers_is_valid(self):
        self.assertTrue(self.v.is_valid([123, 456]))

    def test_tuple_of_integers_is_valid(self):
        self.assertTrue(self.v.is_valid((123, 456)))

    def test_list_of_strings_is_valid(self):
        self.assertTrue(self.v.is_valid(['123', '456']))

    def test_tuple_of_strings_is_valid(self):
        self.assertTrue(self.v.is_valid(('123', '456')))

    def test_list_of_strings_converts(self):
        self.assertEqual(
            self.v.convert(['123', '456']),
            [123, 456]
        )

    def test_tuple_of_strings_converts(self):
        self.assertEqual(
            self.v.convert(('123', '456')),
            [123, 456]
        )

    def test_list_of_integers_converts(self):
        self.assertEqual(
            self.v.convert([123, 456]),
            [123, 456]
        )

    def test_tuple_of_integers_converts(self):
        self.assertEqual(
            self.v.convert((123, 456)),
            [123, 456]
        )


class TestDictValidator(TestCase):
    sub_schema = {'author': validation.StringValidator(True),
                  'committer': validation.StringValidator(),
                  'message': validation.StringValidator()}

    def setUp(self):
        self.v = validation.DictValidator(sub_schema=self.sub_schema)

    def test_handles_None(self):
        self.assertFalse(self.v.is_valid(None))
        self.v.allow_none = True
        self.assertTrue(self.v.is_valid(None))

    def test_skips_missing_optional_keys(self):
        data = {'committer': 'Ian', 'message': 'Foo'}
        self.assertTrue(self.v.is_valid(data))

    def test_fails_missing_required_keys(self):
        data = {'author': 'Ian', 'message': 'Foo'}
        self.assertFalse(self.v.is_valid(data))

    def test_accepts_list_of_tuples(self):
        data = {'committer': 'Ian', 'message': 'Foo'}.items()
        self.assertTrue(self.v.is_valid(data))

    def test_converts_list_of_tuples(self):
        data = {'committer': 'Ian', 'message': 'Foo'}
        self.assertEqual(
            self.v.convert(data.items()),
            data
        )

    def test_converts_dicts(self):
        data = {'committer': 'Ian', 'message': 'Foo'}
        self.assertEqual(
            self.v.convert(data),
            data
        )


class TestStringValidator(TestCase):
    def setUp(self):
        self.v = validation.StringValidator()

    def test_fails_with_None(self):
        self.assertFalse(self.v.is_valid(None))

if __name__ == '__main__':
    import unittest
    unittest.main()
