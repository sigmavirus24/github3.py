# -*- coding: utf-8 -*-
from collections import Callable
from datetime import datetime, timedelta, tzinfo
from requests.compat import basestring
import re

# with thanks to https://code.google.com/p/jquery-localtime/issues/detail?id=4
ISO_8601 = re.compile("^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[0-1]|0"
                      "[1-9]|[1-2][0-9])(T(2[0-3]|[0-1][0-9]):([0-5][0-9]):([0"
                      "-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[0-1][0-9]):[0-5]["
                      "0-9])?)?$")


def timestamp_parameter(timestamp, allow_none=True):

    if timestamp is None:
        if allow_none:
            return None
        raise ValueError("Timestamp value cannot be None")

    if isinstance(timestamp, datetime):
        return timestamp.isoformat()

    if isinstance(timestamp, basestring):
        if not ISO_8601.match(timestamp):
            raise ValueError(("Invalid timestamp: %s is not a valid ISO-8601"
                              " formatted date") % timestamp)
        return timestamp

    raise ValueError("Cannot accept type %s for timestamp" % type(timestamp))


class UTC(tzinfo):
    """Yet another UTC reimplementation, to avoid a dependency on pytz or
    dateutil."""

    ZERO = timedelta(0)

    def __repr__(self):
        return 'UTC()'

    def dst(self, dt):
        return self.ZERO

    def tzname(self, dt):
        return 'UTC'

    def utcoffset(self, dt):
        return self.ZERO


def stream_response_to_file(response, path=None):
    pre_opened = False
    fd = None
    if path:
        if isinstance(getattr(path, 'write', None), Callable):
            pre_opened = True
            fd = path
        else:
            fd = open(path, 'wb')
    else:
        header = response.headers['content-disposition']
        i = header.find('filename=') + len('filename=')
        fd = open(header[i:], 'wb')

    for chunk in response.iter_content(chunk_size=512):
        fd.write(chunk)

    if not pre_opened:
        fd.close()
