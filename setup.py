#!/usr/bin/env python

import sys
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] in ("submit", "publish"):
    os.system("python setup.py sdist upload")
    sys.exit()

packages = ["github3"]
requires = ["requests>=0.12.1"]

setup(
    name="github3",
    version="0.1-pre-alpha",
    description="Python wrapper for the GitHub API (http://developer.github.com/v3)",
    long_description="\n\n".join([open("README.rst").read(), 
        open("HISTORY.rst").read()]),
    author="graffatcolmingov",
    author_email="graffatcolmingov@gmail.com",
    url="https://github.com/sigmavirus24/github3.py",
    packages=packages,
    package_data={'': ['LICENSE']},
    install_requires=requires,
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: Implementation :: CPython',
        ),
    )
