from datetime import datetime
from github3 import validation
from tests.utils import TestCase, patch


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

    def test_lists_of_invalid_tupes_are_invalid(self):
        self.assertFalse(self.v.is_valid([(1, ), (2, )]))

    def test_None_converts(self):
        self.v.allow_none = True
        self.assertEqual(None, self.v.convert(None))


class TestStringValidator(TestCase):
    def setUp(self):
        self.v = validation.StringValidator()

    def test_fails_with_None(self):
        self.assertFalse(self.v.is_valid(None))

    def test_integer_is_valid(self):
        self.assertTrue(self.v.is_valid(123))

    def test_string_is_valid(self):
        self.assertTrue(self.v.is_valid('123'))

    def test_converts_integer(self):
        self.assertEqual(self.v.convert(123), '123')

    def test_converts_string(self):
        self.assertEqual(self.v.convert('123'), '123')


class TestDateValidator(TestCase):
    def setUp(self):
        self.v = validation.DateValidator()
        self.datetime = datetime(2010, 6, 1, 12, 15, 30)
        self.datestrings = ('2010-06-01', '2010-06-01T12:15:30',
                            '2010-06-01T12:14:30.12321+02:00',
                            '2010-06-01T12:14:30.12321-02:00',
                            '2010-06-01T12:14:30.2115Z',
                            )

    def test_datetime_is_valid(self):
        self.assertTrue(self.v.is_valid(self.datetime))

    def test_datetime_converts(self):
        self.assertEqual('2010-06-01T12:15:30', self.v.convert(self.datetime))

    def test_string_is_valid(self):
        for timestamp in self.datestrings:
            self.assertTrue(self.v.is_valid(timestamp))

    def test_string_convert(self):
        for timestamp in self.datestrings:
            self.assertEqual(timestamp, self.v.convert(timestamp))

    def test_None_is_invalid(self):
        self.assertFalse(self.v.is_valid(None))

    def test_None_is_valid(self):
        self.v.allow_none = True
        self.assertTrue(self.v.is_valid(None))

    def test_None_converts(self):
        self.v.allow_none = True
        self.assertEqual(None, self.v.convert(None))

    def test_invalid_string_does_not_convert(self):
        self.assertRaises(ValueError, self.v.convert, 'foo')

    def test_invalid_type_raises_error_during_convert(self):
        self.assertRaises(ValueError, self.v.convert, 123)


class TestBaseValidator(TestCase):
    def setUp(self):
        self.v = validation.BaseValidator()

    def test_is_valid_raises_exception(self):
        self.assertRaises(NotImplementedError, self.v.is_valid, None)


class TestSchemaValidator(TestCase):
    def setUp(self):
        self.schema = {
            'author': validation.StringValidator(required=True),
            'committer': validation.StringValidator(),
            'date': validation.DateValidator(),
            'since': validation.IntegerValidator(),
        }

    def test_validate_is_called_upon_initialization(self):
        with patch.object(validation.SchemaValidator, 'validate') as v:
            validation.SchemaValidator({'author': 'Ian'}, self.schema)
            v.assert_called()

    def test_removes_extra_keys(self):
        data = {'author': 'Ian', 'irrelevant': 'spam'}
        v = validation.SchemaValidator(data, self.schema)
        self.assertTrue('irrelevant' not in v)

    def test_raises_ValueError_for_required_parameter(self):
        data = {'committer': 'Ian'}
        self.assertRaises(ValueError, validation.SchemaValidator, data,
                          self.schema)

    def test_skips_keys_that_are_not_present(self):
        data = {'author': 'Ian'}
        v = validation.SchemaValidator(data, self.schema)
        self.assertTrue('author' in v)
        self.assertTrue('committer' not in v)
        self.assertTrue('date' not in v)
        self.assertTrue('since' not in v)

    def test_raises_ValueError_with_invalid_required_parameter(self):
        data = {'author': None}
        self.assertRaises(ValueError, validation.SchemaValidator, data,
                          self.schema)

    def test_deletes_key_when_invalid_but_not_required(self):
        data = {'author': 'Ian', 'committer': None}
        v = validation.SchemaValidator(data, self.schema)
        self.assertTrue('author' in v)
        self.assertTrue('committer' not in v)
