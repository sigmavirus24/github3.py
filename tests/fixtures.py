import os
import sys
from io import BytesIO


def path(name, mode="r"):
    return open(f"tests/json/{name}", mode)


def content(path_name):
    content = path(path_name).read().strip()
    iterable = f"[{content}]"
    content = content.encode()
    iterable = iterable.encode()
    return BytesIO(content), BytesIO(iterable)


default = {}
iterable = {}
for file in os.listdir("tests/json/"):
    default[file], iterable[file] = content(file)
