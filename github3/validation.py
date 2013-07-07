from requests.compat import basestring
from datetime import datetime
import re


class ParameterValidator(dict):
    """This class is used to validate parameters sent to methods.

    It will use a slightly strict validation method and be capable of being
    passed directly to requests or ``json.dumps``.

    """

    def __init__(self, params, schema):
        self.schema = schema
        self.params = params
        self.update(**self.params)
        self.validate()

    def validate(self):
        params_copy = self.params.copy()
        for key in params_copy:
            if key not in self.schema:
                self.remove_key(key)
                # We can not pass extra information onto GitHub
                # If we let items pass through that we don't validate, this
                # would be a pointless exercise

        for key, validator in self.schema.items():
            if key not in self.params:
                continue
            value = self.params[key]
            if not validator.is_valid(value):
                if not validator.allow_none:
                    raise ValueError(
                        'Key "{0}" is required but is invalid.'.format(key)
                    )
                self.remove_key(key)
            else:
                self.set_key(key, validator.convert(value))

    def remove_key(self, key):
        del(self.params[key], self[key])

    def set_key(self, key, value):
        self.params[key] = self[key] = value

    def update(self, **kwargs):
        super(ParameterValidator, self).update(**kwargs)
        self.params.update(**kwargs)
        self.validate()


class BaseValidator(object):
    def __init__(self, allow_none=False, sub_schema=None):
        self.allow_none = allow_none
        self.sub_schema = sub_schema or {}

    def none(self, o):
        if self.allow_none and o is None:
            return True
        return False

    def is_valid(self, obj):
        raise NotImplementedError(
            "You can not use the BaseValidator's is_vaild method"
        )


class DateValidator(BaseValidator):
    # with thanks to
    # https://code.google.com/p/jquery-localtime/issues/detail?id=4
    ISO_8601 = re.compile(
        "^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[0-1]|0"
        "[1-9]|[1-2][0-9])(T(2[0-3]|[0-1][0-9]):([0-5][0-9]):([0"
        "-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[0-1][0-9]):[0-5]["
        "0-9])?)?$"
    )

    def is_valid(self, timestamp):
        if self.none(timestamp):
            return True

        return (isinstance(timestamp, datetime) or
                (isinstance(timestamp, basestring) and
                 DateValidator.ISO_8601.match(timestamp)))

    def convert(self, timestamp):
        if timestamp is None:
            return None

        if isinstance(timestamp, datetime):
            return timestamp.isoformat()

        if isinstance(timestamp, basestring):
            if not DateValidator.ISO_8601.match(timestamp):
                raise ValueError(
                    ("Invalid timestamp: %s is not a valid ISO-8601"
                     " formatted date") % timestamp)
            return timestamp

        raise ValueError(
            "Cannot accept type %s for timestamp" % type(timestamp))


class StringValidator(BaseValidator):
    def is_valid(self, string):
        if isinstance(string, basestring):
            return True

        if not self.allow_none and string is None:
            return False

        try:
            str(string)
        except:
            return False

        return True

    def convert(self, string):
        return string if isinstance(string, basestring) else str(string)


class DictValidator(BaseValidator):
    def is_valid(self, dictionary):
        try:
            d = dict(dictionary)
        except TypeError:
            return self.none(dictionary)
        except ValueError:
            return False

        schema_items = self.sub_schema.items()
        return all(
            [v.is_valid(d.get(k)) for (k, v) in schema_items]
        )

    def convert(self, dictionary):
        if self.none(dictionary):
            return None

        dictionary = dict(dictionary)
        for k, v in self.sub_schema.items():
            if dictionary.get(k):
                dictionary[k] = v.convert(dictionary[k])
        return dictionary


class ListValidator(BaseValidator):
    def is_valid(self, lyst):
        try:
            lyst = list(lyst)
        except TypeError:
            return self.none(lyst)

        is_valid = self.sub_schema.is_valid
        return all([is_valid(i) for i in lyst])

    def convert(self, lyst):
        if self.none(lyst):
            return None

        convert = self.sub_schema.convert
        return [convert(i) for i in lyst]


class IntegerValidator(BaseValidator):
    def is_valid(self, integer):
        try:
            integer = int(integer)
        except ValueError:
            return False
        except TypeError:
            if integer is not None:
                raise
            return self.none(integer)
        return True

    def convert(self, integer):
        return int(integer)
