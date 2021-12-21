import textwrap

import github3

i = github3.issue("kennethreitz", "requests", 868)
for line in textwrap.wrap(i.body_text, 78, replace_whitespace=False):
    print(line)
