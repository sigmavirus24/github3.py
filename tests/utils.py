import requests
from mock import patch
from io import BytesIO
import expecter


def generate_response(path_name, status_code=200, encoding='utf-8'):
    r = requests.Response()
    r.status_code = status_code
    r.encoding = encoding
    if path_name:
        content = path(path_name)
        r.raw = BytesIO(content.read().encode())
    else:
        r.raw = BytesIO()
    return r


def path(name, mode='r'):
    return open('tests/json/{0}'.format(name), mode)


def patch_request(method='request'):
    def decorator(func):
        return patch.object(requests.sessions.Session, method)(func)
    return decorator


class CustomExpecter(expecter.expect):
    def is_not_None(self):
        assert self._actual is not None, (
                'Expected anything but None but got it.'
                )

    def is_None(self):
        assert self._actual is None, (
                'Expected None but got %s' % repr(self._actual)
                )

    def is_True(self):
        assert self._actual is True, (
                'Expected True but got %s' % repr(self._actual)
                )

    def is_False(self):
        assert self._actual is False, (
                'Expected False but got %s' % repr(self._actual)
                )

    def list_of(self, cls):
        for actual in self._actual:
            CustomExpecter(actual).isinstance(cls)

expect = CustomExpecter
