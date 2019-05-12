# -*- coding: utf-8 -*-
"""Packaging logic."""
import os
import re
import sys
import warnings

import setuptools
import setuptools.command.test

kwargs = {}
requires = []
packages = [
    "github3",
    "github3.gists",
    "github3.repos",
    "github3.issues",
    "github3.search",
]

SNI_requirements = [
    'pyOpenSSL',
    'ndg-httpsclient',
    'pyasn1',
]

kwargs['tests_require'] = ['betamax>=0.8.0', 'pytest>2.3.5',
                           'betamax-matchers>=0.1.0']
if sys.version_info < (3, 0):
    kwargs['tests_require'].append('unittest2 ==0.5.1')
if sys.version_info < (3, 3):
    kwargs['tests_require'].append('mock')

if sys.argv[-1] in ("submit", "publish"):
    os.system("python setup.py bdist_wheel sdist upload")
    sys.exit()

requires.extend([
    "requests >= 2.18",
    "uritemplate >= 3.0.0",
    "python-dateutil >= 2.6.0",
    "jwcrypto >= 0.5.0",
])

__version__ = ''
with open('src/github3/__about__.py', 'r') as fd:
    reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
    for line in fd:
        m = reg.match(line)
        if m:
            __version__ = m.group(1)
            break

if not __version__:
    raise RuntimeError('Cannot find version information')


class PyTest(setuptools.command.test.test):  # noqa: D101
    def finalize_options(self):  # noqa: D102
        setuptools.command.test.test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):  # noqa: D102
        # import here, cause outside the eggs aren't loaded
        import pytest
        warnings.warn("pyton setup.py test support is deprecated.",
                      DeprecationWarning)
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setuptools.setup(
    name="github3.py",
    version=__version__,
    description=("Python wrapper for the GitHub API"
                 "(http://developer.github.com/v3)"),
    long_description=open("README.rst").read(),
    license='3-clause BSD',
    author="Ian Stapleton Cordasco",
    author_email="graffatcolmingov@gmail.com",
    url="https://github3.readthedocs.io",
    packages=packages,
    package_dir={"": "src"},
    install_requires=requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    extras_require={
        'test': kwargs['tests_require'],
        'sni': SNI_requirements,
    },
    cmdclass={'test': PyTest},
    **kwargs
)
