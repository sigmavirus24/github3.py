#!/usr/bin/env python

import sys
import os
import github3

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
    name="github3.py",
    version=github3.__version__,
    description="Python wrapper for the GitHub API (http://developer.github.com/v3)",
    long_description="\n\n".join([open("README.rst").read(), 
        open("HISTORY.rst").read()]),
    license=open('LICENSE').read(),
    author=github3.__author__,
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
