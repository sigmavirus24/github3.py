from requests import Response
from io import BytesIO


def generate_response(content, status_code=200, encoding='utf-8'):
    r = Response()
    r.status_code = status_code
    r.encoding = encoding
    r.raw = BytesIO(content.read().encode())
    return r


def path(name):
    return 'mock_tests/json/{0}'.format(name)
