#!/usr/bin/env python

import sys
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] in ("submit", "publish"):
    os.system("python setup.py sdist upload")
    sys.exit()

packages = ["github3"]
requires = ["requests>=0.13.8"]

__version__ = ''
with open('github3/__init__.py', 'r') as fd:
    reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
    for line in fd:
        m = reg.match(line)
        if m:
            __version__ = m.group(1)
            break

if not __version__:
    raise RuntimeError('Cannot find version information')

setup(
    name="github3.py",
    version=__version__,
    description="Python wrapper for the GitHub API (http://developer.github.com/v3)",
    long_description="\n\n".join([open("README.rst").read(), 
        open("HISTORY.rst").read()]),
    license=open('LICENSE').read(),
    author="Ian Cordasco",
    author_email="graffatcolmingov@gmail.com",
    url="https://github3py.readthedocs.org",
    packages=packages,
    package_data={'': ['LICENSE', 'AUTHORS.rst']},
    include_package_data=True,
    install_requires=requires,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: Implementation :: CPython',
        ],
    )
