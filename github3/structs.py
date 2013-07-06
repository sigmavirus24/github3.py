from collections import Iterator
from github3.models import GitHubCore, urlparse
from requests.compat import basestring
from datetime import datetime
import re


class GitHubIterator(GitHubCore, Iterator):
    """The :class:`GitHubIterator` class powers all of the iter_* methods."""
    def __init__(self, count, url, cls, session, params=None, etag=None):
        GitHubCore.__init__(self, {}, session)
        #: Original number of items requested
        self.original = count
        #: Number of items left in the iterator
        self.count = count
        #: URL the class used to make it's first GET
        self.url = url
        self._api = self.url
        #: Class being used to cast all items to
        self.cls = cls
        #: Parameters of the query string
        self.params = params
        self._remove_none(self.params)
        # We do not set this from the parameter sent. We want this to
        # represent the ETag header returned by GitHub no matter what.
        # If this is not None, then it won't be set from the response and
        # that's not what we want.
        #: The ETag Header value returned by GitHub
        self.etag = None
        #: Headers generated for the GET request
        self.headers = {}
        #: The last response seen
        self.last_response = None
        #: Last status code received
        self.last_status = 0

        if etag:
            self.headers = {'If-None-Match': etag}

    def __repr__(self):
        path = urlparse(self.url).path
        return '<GitHubIterator [{0}, {1}]>'.format(self.count, path)

    def __iter__(self):
        url, params, cls = self.url, self.params, self.cls
        headers = self.headers

        while (self.count == -1 or self.count > 0) and url:
            response = self._get(url, params=params, headers=headers)
            self.last_response = response
            self.last_status = response.status_code
            if params:
                params = None  # rel_next already has the params

            if not self.etag and response.headers.get('ETag'):
                self.etag = response.headers.get('ETag')

            json = self._json(response, 200)

            if json is None:
                break

            # languages returns a single dict. We want the items.
            if isinstance(json, dict):
                json = json.items()

            for i in json:
                yield cls(i, self) if issubclass(cls, GitHubCore) else cls(i)
                self.count -= 1 if self.count > 0 else 0
                if self.count == 0:
                    break

            rel_next = response.links.get('next', {})
            url = rel_next.get('url', '')

    def __next__(self):
        if not hasattr(self, '__i__'):
            self.__i__ = self.__iter__()
        return next(self.__i__)

    def refresh(self, conditional=False):
        self.count = self.original
        if conditional:
            self.headers['If-None-Match'] = self.etag
        self.__i__ = self.__iter__()
        return self

    def next(self):
        return self.__next__()


class ParameterValidator(dict):
    """This class is used to validate parameters sent to methods.

    It will use a slightly strict validation method and be capable of being
    passed directly to requests or ``json.dumps``.

    """

    def __init__(self, params, schema):
        self.params = params
        self.update(self.params)
        self.schema = schema
        self.validate()

    def validate(self):
        params_copy = self.params.copy()
        for key in params_copy:
            if key not in self.schema:
                self.remove_key(key)
                # We can not pass extra information onto GitHub
                # If we let items pass through that we don't validate, this
                # would be a pointless exercise

        for key, (required, validator) in self.schema.items():
            if key not in self.params:
                continue
            value = self.params[key]
            if not validator.is_valid(value):
                if required:
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


class BaseValidator(object):
    def __init__(self, allow_none=False, sub_schema=None):
        self.allow_none = allow_none
        self.sub_schema = sub_schema or {}

    def none(self, o):
        if self.allow_none and o is None:
            return True

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
            dictionary = dict(dictionary)
        except ValueError:
            return False

        schema_items = self.sub_schema.items()
        return any(
            [v.is_valid(dictionary[k]) for (k, v) in schema_items]
        )

    def convert(self, dictionary):
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
            return False

        is_valid = self.sub_schema.is_valid
        return all([is_valid(i) for i in lyst])

    def convert(self, lyst):
        convert = self.sub_schema.convert
        return [convert(i) for i in lyst]
