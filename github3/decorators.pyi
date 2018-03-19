from typing import (
    Any,
)

import io

import requests


class RequestsStringIO(io.BytesIO):
    def read(self, n: int=-1, *args, **kwargs) -> bytes:  # type: ignore
        ...


# These decorators are broken until there's a solution to
# https://github.com/python/typing/issues/193
# https://github.com/python/mypy/issues/1317
def requires_auth(func: Any) -> Any:
    ...


def requires_basic_auth(func: Any) -> Any:
    ...


def requires_app_credentials(func: Any) -> Any:
    ...


def generate_fake_error_message(
    msg: str,
    status_code: int=401,
    encoding: str='utf-8',
) -> requests.models.Response:
    ...
