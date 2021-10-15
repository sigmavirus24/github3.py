"""Packaging logic."""
import re

import setuptools

__version__ = ""
with open("src/github3/__about__.py") as fd:
    reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
    for line in fd:
        m = reg.match(line)
        if m:
            __version__ = m.group(1)
            break

setuptools.setup(
    version=__version__,
)
