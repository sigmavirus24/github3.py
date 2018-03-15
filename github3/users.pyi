from . import models

class _User(models.GitHubCore):
    ...


class User(_User):
    ...


class ShortUser(_User):
    _refresh_to = User


class Contributor(_User):
    ...


class AuthenticatedUser(User):
    ...


class Email(models.GitHubCore):
    ...


class Key(models.GitHubCore):
    ...
