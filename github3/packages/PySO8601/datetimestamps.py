from datetime import datetime, date, timedelta
from .regexs import TIME_FORMATS, DATE_FORMATS
from .utility import ParseError
from .timezones import Timezone

ONE_DAY = timedelta(days=1)


def parse_date(datestring):
    """Attepmts to parse an ISO8601 formatted ``datestring``.

    Returns a ``datetime.datetime`` object.
    """
    datestring = str(datestring).strip()

    if not datestring[0].isdigit():
        raise ParseError()

    for regex, pattern in DATE_FORMATS:
        if regex.match(datestring):
            found = regex.search(datestring).groupdict()

            value = found['date']

            if 'W' in found['date'].upper():
                value = found['date'][:-1] + str(int(found['date'][-1:]) - 1)

            if 'separator' in found:
                value += found['separator']

            if 'time' in found:
                value += found['time']

            dt = datetime.utcnow().strptime(value, pattern)

            if 'fraction' in found and found['fraction'] is not None:
                dt = dt.replace(microsecond=int(found['fraction'][1:]))

            if 'timezone' in found and found['timezone'] is not None:
                dt = dt.replace(tzinfo=Timezone(found.get('timezone', '')))

            return dt

    return parse_time(datestring)


def parse_time(timestring):
    """Attepmts to parse an ISO8601 formatted ``timestring``.

    Returns a ``datetime.datetime`` object.
    """
    timestring = str(timestring).strip()

    for regex, pattern in TIME_FORMATS:
        if regex.match(timestring):
            found = regex.search(timestring).groupdict()

            dt = datetime.utcnow().strptime(found['time'], pattern)
            dt = datetime.combine(date.today(), dt.time())

            if 'fraction' in found and found['fraction'] is not None:
                dt = dt.replace(microsecond=int(found['fraction'][1:]))

            if 'timezone' in found and found['timezone'] is not None:
                dt = dt.replace(tzinfo=Timezone(found.get('timezone', '')))

            return dt

    raise ParseError()
