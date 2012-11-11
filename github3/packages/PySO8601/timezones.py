import datetime
import re


class Timezone(datetime.tzinfo):
    """A subclass of ``datetime.tzinfo`` which handles timezone offsets for the
    various other methods in the module.

    ``tzstring`` accepts a valid ISO8601 timezone string or ``None`` for UTC.
    """
    _ZERO = datetime.timedelta(0)
    _regex = re.compile(r'^(?P<prefix>\+|-)(?P<hours>\d{2})'
            '(:?(?P<mins>\d{2}))?')

    def __init__(self, tzstring=None):
        self.__offset = self._ZERO
        self.__name = 'UTC'

        if tzstring is None or tzstring.strip() in ('Z', ''):
            return

        found = self._regex.search(tzstring.strip()).groupdict()
        prefix, hours, mins = (found['prefix'], int(found['hours']),
                int(found['mins'] or 0))

        self.__name = "UTC%s%02d:%02d" % (prefix, hours, mins)

        if prefix == '-':
            hours, mins = -hours, -mins

        self.__offset = datetime.timedelta(hours=hours,
                                           minutes=mins)

    def utcoffset(self, dt):
        return self.__offset

    def dst(self, dt):
        return self._ZERO

    def __repr__(self):
        return "<Timezone %s>" % self.__name

    def __str__(self):
        return self.__name
