import requests

from github3 import __version__
from logging import getLogger

__url_cache__ = {}
__logs__ = getLogger(__package__)


class GitHubSession(requests.Session):
    def __init__(self):
        super(GitHubSession, self).__init__()
        self.headers.update({
            # Only accept JSON responses
            'Accept': 'application/vnd.github.v3.full+json',
            # Only accept UTF-8 encoded data
            'Accept-Charset': 'utf-8',
            # Always sending JSON
            'Content-Type': "application/json",
            # Set our own custom User-Agent string
            'User-Agent': 'github3.py/{0}'.format(__version__),
            })
        self.base_url = 'https://api.github.com'

    def basic_auth(self, username, password):
        """Set the Basic Auth credentials on this Session.

        :param str username: Your GitHub username
        :param str password: Your GitHub password
        """
        if not (username and password):
            return

        self.auth = (username, password)

    def build_url(self, *args, **kwargs):
        """Builds a new API url from scratch."""
        parts = [kwargs.get('base_url') or self.base_url]
        parts.extend(args)
        parts = [str(p) for p in parts]
        key = tuple(parts)
        __logs__.info('Building a url from %s', key)
        if not key in __url_cache__:
            __logs__.info('Missed the cache building the url')
            __url_cache__[key] = '/'.join(parts)
        return __url_cache__[key]

    def token_auth(self, token):
        """Use an application token for authentication.

        :param str token: Application token retrieved from GitHub's
            /authorizations endpoint
        """
        if not token:
            return

        self.headers.update({
            'Authorization': 'token {0}'.format(token)
            })

    def oauth2_auth(self, client_id, client_secret):
        """Use OAuth2 for authentication.

        It is suggested you install requests-oauthlib to use this.

        :param str client_id: Client ID retrieved from GitHub
        :param str client_secret: Client secret retrieved from GitHub
        """
        raise NotImplementedError('These features are not implemented yet')
