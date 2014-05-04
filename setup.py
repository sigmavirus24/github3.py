# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import os
import re

from setuptools import setup
from setuptools.command.test import test as TestCommand

kwargs = {}
requires = []
packages = [
    "github3",
    "github3.gists",
    "github3.repos",
    "github3.issues",
    "github3.search",
]

kwargs['tests_require'] = ['betamax >=0.2.0', 'pytest']
if sys.version_info < (3, 0):
    kwargs['tests_require'].append('unittest2 ==0.5.1')
if sys.version_info < (3, 3):
    kwargs['tests_require'].append('mock ==1.0.1')

if sys.argv[-1] in ("submit", "publish"):
    os.system("python setup.py bdist_wheel sdist upload")
    sys.exit()

requires.extend(["requests >= 2.0", "uritemplate.py >= 0.2.0"])

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


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name="github3.py",
    version=__version__,
    description=("Python wrapper for the GitHub API"
                 "(http://developer.github.com/v3)"),
    long_description="\n\n".join([open("README.rst").read(),
                                  open("HISTORY.rst").read()]),
    license=open('LICENSE').read(),
    author="Ian Cordasco",
    author_email="graffatcolmingov@gmail.com",
    url="https://github3py.readthedocs.org",
    packages=packages,
    install_requires=requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    extras_require={'test': kwargs['tests_require']},
    cmdclass={'test': PyTest},
    **kwargs
)
