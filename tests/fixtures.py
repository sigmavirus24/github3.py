from io import BytesIO
import os
import sys


def path(name, mode='r'):
    return open('tests/json/{0}'.format(name), mode)


def content(path_name):
    content = path(path_name).read().strip()
    iterable = '[{0}]'.format(content)
    if sys.version_info > (3, 0):
        content = content.encode()
        iterable = iterable.encode()
    return BytesIO(content), BytesIO(iterable)


default = {}
iterable = {}
for file in os.listdir('tests/json/'):
    default[file], iterable[file] = content(file)
