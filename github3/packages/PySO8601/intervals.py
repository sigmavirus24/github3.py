from .utility import ParseError
from .durations import parse_duration
from .datetimestamps import parse_date


def parse_interval(interval):
    """Attepmts to parse an ISO8601 formatted ``interval``.

    Returns a tuple of ``datetime.datetime`` and ``datetime.timedelta``
    objects, order dependent on ``interval``.
    """
    a, b = str(interval).upper().strip().split('/')

    if a[0] is 'P' and b[0] is 'P':
        raise ParseError()

    if a[0] is 'P':
        a = parse_duration(a)
    else:
        a = parse_date(a)

    if b[0] is 'P':
        b = parse_duration(b)
    else:
        b = parse_date(b)

    return a, b
