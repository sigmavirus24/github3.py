#!/usr/bin/env python
import sys
import os
from github3 import login
from getpass import getpass

try:
    import readline
    readline.parse_and_bind('tab: complete')
except ImportError:
    pass

if hasattr(__builtins__, 'raw_input'):
    prompt = raw_input
else:
    prompt = input


def prompt_user(prompt_str):
    val = ''
    while not val:
        val = prompt(prompt_str)
    return val

if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help', '-?'):
    print("Usage: {0} [-h|-?|--help]".format(sys.argv[0]))
    print("Simple issue reporting script for github3.py\n")
    print("If you're reporting a bug, please save a traceback to a file")
    print("and supply the filename when filing the bug report. Please be")
    print("as descriptive as possible.\n\n")
    print("  -h, -?, --help  Print this message and exit")
    sys.exit(0)

username = ''
password = ''

username = prompt_user('Enter GitHub username: ')

while not password:
    password = getpass('Password for {0}: '.format(username))

g = login(username, password)
repo = g.repository('sigmavirus24', 'github3.py')

title = prompt_user('Title/summary: ')
issue_type = prompt_user('Bug or feature request? ')

traceback = None
if issue_type.lower() == 'bug':
    tb_file = prompt_user('Filename with traceback: ')
    if os.path.isfile(tb_file):
        traceback = open(tb_file).read()

description = prompt_user('Description: ')

body = """**Issue type**: {0}

------

**Traceback**:
```
{1}
```

------

**Description**:
{2}

------

*Generated with github3.py using the report_issue script*
""".format(issue_type, traceback, description)

i = repo.create_issue(title, body)

print(i.html_url)
