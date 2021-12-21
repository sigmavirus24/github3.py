#!/usr/bin/env python
import os
import sys
from getpass import getpass

from github3 import login

try:
    import readline

    readline.parse_and_bind("tab: complete")
except ImportError:
    pass


def prompt_user(prompt_str):
    return input(prompt_str).strip() or prompt_user(prompt_str)


if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help", "-?"):
    print(f"Usage: {sys.argv[0]} [-h|-?|--help]")
    print("Simple issue reporting script for github3.py\n")
    print("If you're reporting a bug, please save a traceback to a file")
    print("and supply the filename when filing the bug report. Please be")
    print("as descriptive as possible.\n\n")
    print("  -h, -?, --help  Print this message and exit")
    sys.exit(0)

username = ""
password = ""

username = prompt_user("Enter GitHub username: ")

while not password:
    password = getpass(f"Password for {username}: ")

g = login(username, password)
repo = g.repository("sigmavirus24", "github3.py")

title = prompt_user("Title/summary: ")
issue_type = prompt_user("Bug or feature request? ")

traceback = None
if issue_type.lower() == "bug":
    tb_file = prompt_user("Filename with traceback: ")
    if os.path.isfile(tb_file):
        traceback = open(tb_file).read()

description = prompt_user("Description: ")

body = """**Issue type**: {}

------

**Traceback**:
```
{}
```

------

**Description**:
{}

------

*Generated with github3.py using the report_issue script*
""".format(
    issue_type, traceback, description
)

i = repo.create_issue(title, body)

print(i.html_url)
