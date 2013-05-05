from github3.structs import GitHubIterator
from github3.users import User
import logging

stderr = logging.StreamHandler()
l = logging.getLogger('github3')
l.addHandler(stderr)
l.setLevel(logging.DEBUG)

i = GitHubIterator(10, 'https://api.github.com/users', User, None)
