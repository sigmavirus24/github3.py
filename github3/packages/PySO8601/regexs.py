import re

"""
Years:
    YYYY
Calendar Dates:
    YYYY-MM-DD
    YYYY-MM
    YYYYMMDD
    YYMMDD
Week Dates:
    YYYY-Www-D
    YYYY-Www
    YYYYWwwD
    YYYYWww
Ordinal Dates:
    YYYY-DDD
    YYYYDDD
Times:
    hh:mm:ss
    hh:mm
    hhmmss
    hhmm
    <time>Z
    <time>+|-hh:mm
    <time>+|-hhmm
    <time>+|-hh
"""

FRACTION = r'(?P<fraction>\.\d+)?'

TIMEZONE = r'(?P<timezone>Z|(\+|-)(\d{2})(:?\d{2})?)?$'

TIME_FORMATS_EXTENDED = (
    (r'(?P<time>\d{2}:\d{2}:\d{2})' + FRACTION + TIMEZONE, '%H:%M:%S'),
    (r'(?P<time>\d{2}:\d{2})' + TIMEZONE, '%H:%M'),
    )

TIME_FORMATS_BASIC = (
    # Times
    (r'(?P<time>\d{2}\d{2}\d{2})' + FRACTION + TIMEZONE, '%H%M%S'),
    (r'(?P<time>\d{4})' + TIMEZONE, '%H%M'),
    (r'(?P<time>\d{2})' + TIMEZONE, '%H'),
    )

TIME_FORMATS = tuple(
    (re.compile(r'^' + r), f) for r, f in (TIME_FORMATS_EXTENDED +
        TIME_FORMATS_BASIC)
    )

SEPARATORS = (
    (r'(?P<separator>T)', 'T'),
    (r'(?P<separator>\s)', ' '),
    )

DATE_FORMATS_EXTENDED = (
    # Dates
    (r'(?P<date>\d{4}-\d{2}-\d{2})', '%Y-%m-%d'),
    (r'(?P<date>\d{4}-\d{2})', '%Y-%m'),

    # Week Dates
    (r'(?P<date>\d{4}-W\d{2}-\d)', '%Y-W%U-%w'),
    (r'(?P<date>\d{4}-W\d{2})', '%Y-W%U'),

    # Ordinal Dates
    (r'(?P<date>\d{4}-\d{3})', '%Y-%j'),

    )

DATE_FORMATS_BASIC = (
    # Dates
    (r'(?P<date>\d{8})', '%Y%m%d'),
    (r'(?P<date>\d{6})', '%y%m%d'),
    (r'(?P<date>\d{4})', '%Y'),

    # Week Dates
    (r'(?P<date>\d{4}W\d{3})', '%YW%U%w'),
    (r'(?P<date>\d{4}W\d{2})', '%YW%U'),

    # Ordinal Dates
    (r'(?P<date>\d{7})', '%Y%j'),

    )

DATE_FORMATS = tuple()

for sr, sf in SEPARATORS:
    for dr, df in DATE_FORMATS_EXTENDED:
        for tr, tf in TIME_FORMATS_EXTENDED:
            DATE_FORMATS += (
                (re.compile(r'^' + dr + sr + tr), df + sf + tf),
                )

    for dr, df in DATE_FORMATS_BASIC:
        for tr, tf in TIME_FORMATS_BASIC:
            DATE_FORMATS += (
                (re.compile(r'^' + dr + sr + tr), df + sf + tf),
                )

    for dr, df in DATE_FORMATS_EXTENDED:
        DATE_FORMATS += (
            (re.compile(r'^' + dr + TIMEZONE), df),
            )

    for dr, df in DATE_FORMATS_BASIC:
        DATE_FORMATS += (
            (re.compile(r'^' + dr + TIMEZONE), df),
            )


# DURATIONS ----------

WEEK_DURATION = re.compile(r'''# start
^P # duration designator
(\d+) # capture the number of weeks
W$ # week designator
''', re.VERBOSE)

SIMPLE_DURATION = re.compile(r"""# start
^P                               # duration designator
((?P<years>\d*[\.,]?\d+)Y)?      # year designator
((?P<months>\d*[\.,]?\d+)M)?     # month designator
((?P<days>\d*[\.,]?\d+)D)?       # day designator
(?P<time>T)?                     # time designator
(?(time)                         # time designator lookup;
                                 #   skip next section if
                                 #   reference doesn't exist
  ((?P<hours>\d*[\.,]?\d+)H)?    # hour designator
  ((?P<minutes>\d*[\.,]?\d+)M)?  # minute designator
  ((?P<seconds>\d*[\.,]?\d+)S)?  # second designator
)$
""", re.VERBOSE)

COMBINED_DURATION = re.compile(r"""# start
^P                                 # duration designator
(?P<years>\d{4})?                  # year designator
-?                                 # separator
(?P<months>\d{2})?                 # month designator
-?                                 # separator
(?P<days>\d{2})?                   # day designator
(?P<time>[T|\s])?                  # time designator
(?(time)                           # time designator lookup;
                                   #   skip next section if
                                   #   reference doesn't exist
  (?P<hours>\d{2})                 # hour designator
  :?                               # separator
  (?P<minutes>\d{2})?              # minute designator
  (?(minutes)                      # minutes designator lookup
    :?                             # separator
    (?P<seconds>\d{2})?            # second designator
  )
)$
""", re.VERBOSE)

ELEMENTS = {
    'years': 0,
    'months': 0,
    'days': 0,
    'hours': 0,
    'minutes': 0,
    'seconds': 0,
    }
