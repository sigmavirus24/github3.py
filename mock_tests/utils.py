from requests import Response


def generate_response(content, status_code=200, encoding='utf-8'):
    r = Response()
    r.status_code = status_code
    r.encoding = encoding
    r.raw = content
    return r


def path(name):
    return 'mock_tests/json/{0}'.format(name)
