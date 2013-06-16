from datetime import datetime
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
