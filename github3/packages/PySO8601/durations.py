import datetime
from .regexs import (SIMPLE_DURATION, COMBINED_DURATION, ELEMENTS)
from .utility import ParseError

DAYS_IN_YEAR = 365
MONTHS_IN_YEAR = 12


def _years_to_days(years):
    return years * DAYS_IN_YEAR


def _months_to_days(months):
    return (months * DAYS_IN_YEAR) / MONTHS_IN_YEAR


def parse_duration(duration):
    """Attepmts to parse an ISO8601 formatted ``duration``.

    Returns a ``datetime.timedelta`` object.
    """
    duration = str(duration).upper().strip()

    elements = ELEMENTS.copy()

    for pattern in (SIMPLE_DURATION, COMBINED_DURATION):
        if pattern.match(duration):
            found = pattern.match(duration).groupdict()
            del found['time']

            elements.update(dict((k, int(v or 0))
                                 for k, v
                                 in found.iteritems()))

            return datetime.timedelta(days=(elements['days'] +
                                            _months_to_days(elements['months']) +
                                            _years_to_days(elements['years'])),
                                      hours=elements['hours'],
                                      minutes=elements['minutes'],
                                      seconds=elements['seconds'])

    return ParseError()
