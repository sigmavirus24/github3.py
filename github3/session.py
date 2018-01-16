# -*- coding: utf-8 -*-
import requests
import time

from collections import Callable
from datetime import datetime
from . import __version__
from logging import getLogger
from contextlib import contextmanager
from urllib3.util.url import parse_url

__url_cache__ = {}
__logs__ = getLogger(__package__)


def requires_2fa(response):
    if (response.status_code == 401 and 'X-GitHub-OTP' in response.headers and
            'required' in response.headers['X-GitHub-OTP']):
        return True
    return False


class GitHubSession(requests.Session):
    auth = None
    RATELIMIT_LIMIT_HEADER = 'X-RateLimit-Limit'
    RATELIMIT_REMAINING_HEADER = 'X-RateLimit-Remaining'
    RATELIMIT_RESET_HEADER = 'X-RateLimit-Reset'
    RETRY_AFTER_HEADER = 'Retry-After'
    CORE_RESOURCE = 'core'
    SEARCH_RESOURCE = 'search'
    DEFAULT_SLEEP_PERIOD = 1
    __attrs__ = requests.Session.__attrs__ + ['base_url', 'two_factor_auth_cb']

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
        self.two_factor_auth_cb = None
        self.request_counter = 0
        self._ratelimit_cache = {}
        self.suggested_time_between_requests = self.DEFAULT_SLEEP_PERIOD

    def basic_auth(self, username, password):
        """Set the Basic Auth credentials on this Session.

        :param str username: Your GitHub username
        :param str password: Your GitHub password
        """
        if not (username and password):
            return

        self.auth = (username, password)

        # Disable token authentication
        self.headers.pop('Authorization', None)

    def build_url(self, *args, **kwargs):
        """Builds a new API url from scratch."""
        parts = [kwargs.get('base_url') or self.base_url]
        parts.extend(args)
        parts = [str(p) for p in parts]
        key = tuple(parts)
        __logs__.info('Building a url from %s', key)
        if key not in __url_cache__:
            __logs__.info('Missed the cache building the url')
            __url_cache__[key] = '/'.join(parts)
        return __url_cache__[key]

    def handle_two_factor_auth(self, args, kwargs):
        headers = kwargs.pop('headers', {})
        headers.update({
            'X-GitHub-OTP': str(self.two_factor_auth_cb())
            })
        kwargs.update(headers=headers)
        return super(GitHubSession, self).request(*args, **kwargs)

    def has_auth(self):
        return (self.auth or self.headers.get('Authorization'))

    def oauth2_auth(self, client_id, client_secret):
        """Use OAuth2 for authentication.

        It is suggested you install requests-oauthlib to use this.

        :param str client_id: Client ID retrieved from GitHub
        :param str client_secret: Client secret retrieved from GitHub
        """
        raise NotImplementedError('These features are not implemented yet')

    def _fill_ratelimit_cache(self):
        """Fills rate limit cache with data from server."""
        response = self.get(self.build_url('rate_limit'))
        if response.status_code == 200 and response.content:
            json = response.json()
            if 'resources' in json:
                self._ratelimit_cache = json['resources']
        else:
            __logs__.critical('Cannot fill ratelimit cache')

    def _has_ratelimit_headers(self, headers):
        """Test if rate limit headers are present.

        :param requests.structures.CaseInsensitiveDict headers:
            Headers from response.
        :returns bool:
            True if all necessary headers are present, otherwise False.
        """
        return (
            self.RATELIMIT_LIMIT_HEADER in headers and
            self.RATELIMIT_REMAINING_HEADER in headers and
            self.RATELIMIT_RESET_HEADER in headers)

    def _cache_ratelimit_headers(self, headers, resource=CORE_RESOURCE):
        """Cache rate limit information from response headers.

        :param requests.structures.CaseInsensitiveDict headers:
            Headers from response.
        :param str resource:
            Name of resource to get rate limit for. Either CORE_RESOURCE,
            SEARCH_RESOURCE, or GRAPHQL_RESOURCE.
        :returns dict:
            Dictionary containing remaining rate limit, full rate limit, and
            reset time as POSIX timestamp.  For more information see
            https://developer.github.com/v3/rate_limit/
        """
        if not self._ratelimit_cache:
            self._ratelimit_cache = {}
        if self._has_ratelimit_headers(headers):
            self._ratelimit_cache[resource] = {
                'limit': headers.get(self.RATELIMIT_LIMIT_HEADER),
                'remaining': headers.get(self.RATELIMIT_REMAINING_HEADER),
                'reset': headers.get(self.RATELIMIT_RESET_HEADER)
                }

    def _get_ratelimit(self, resource=CORE_RESOURCE):
        """Get ratelimit information from cache or server.

        :param str resource:
            Name of resource to get rate limit for. Either CORE_RESOURCE,
            SEARCH_RESOURCE, or GRAPHQL_RESOURCE.
        :returns dict:
            Dictionary containing remaining rate limit, full rate limit, and
            reset time as POSIX timestamp.  For more information see
            https://developer.github.com/v3/rate_limit/
        """
        if not (self._ratelimit_cache and resource in self._ratelimit_cache):
            self._fill_ratelimit_cache()
        return self._ratelimit_cache[resource]

    def _wait_for_ratelimit(self, resource=CORE_RESOURCE):
        """Waits until ratelimit refresh if necessary.

        Rate limit is read from headers of last response if this class has a
        last_response member.

        :param str resource:
            Name of resource to get rate limit for. Either CORE_RESOURCE,
            SEARCH_RESOURCE, or GRAPHQL_RESOURCE.
        """
        ratelimit = self._get_ratelimit(resource)
        if int(ratelimit.get('remaining', '0')) < 1:
            reset = datetime.utcfromtimestamp(int(ratelimit.get('reset', '0')))
            delta = reset - datetime.utcnow()
            wait_time = int(delta.total_seconds()) + 2  # For good measure
            if wait_time > 0:
                __logs__.info(
                    'Rate limit reached. Wait for %d sec until %s',
                    wait_time, reset)
                time.sleep(wait_time)

    def _resource_from_url(self, url):
        """Extract rate limited resource from url.

        :param str url:
            URL to check.
        :returns str:
            SEARCH_RESOURCE if first part of path is 'search', otherwise
            CORE_RESOURCE.
        """
        # This method should check 'Accept' header in case github3.py gains
        # functionality to query graphql.
        path = parse_url(url).path
        path_frags = path.split('/') if path else []
        if len(path_frags) > 1 and path_frags[1] == self.SEARCH_RESOURCE:
            return self.SEARCH_RESOURCE
        else:
            return self.CORE_RESOURCE

    def _has_hit_abuse_detection(self, response):
        """Test if response indicates the request hit abuse detection."""
        # bool(response) is False in case of errors. Explicitly test for None.
        if response is None:
            return False
        if response.status_code != 403:
            return False
        return self.RETRY_AFTER_HEADER in response.headers

    def _has_hit_rate_limit(self, response):
        """Test if response indicates that there is no remaining rate limit."""
        # bool(response) is False in case of errors. Explicitly test for None.
        return response is not None and response.status_code == 403

    def _handle_abuse_detection(self, response):
        """Wait for period suggested in response headers.

        Waits exponentially longer everytime it is called.

        Also updates self.suggested_time_between_requests. Consider sleeping
        for suggested time between requests in order to proactively avoid abuse
        detection.
        """
        retry_after = int(response.headers[self.RETRY_AFTER_HEADER])
        __logs__.warn('Status %d: %s', response.status_code, response.json())
        __logs__.info('Retry after: %d', retry_after)
        # Exponential back-off for suggested wait time
        self.suggested_time_between_requests *= 2
        time.sleep(retry_after + self.DEFAULT_SLEEP_PERIOD)

    def request(self, method, url, *args, **kwargs):
        resource = self._resource_from_url(url)
        if url is not self.build_url('rate_limit'):
            self._wait_for_ratelimit(resource=resource)
        while True:
            try:
                response = super(GitHubSession, self).request(
                    method, url, *args, **kwargs)
                self.request_counter += 1
                if requires_2fa(response) and self.two_factor_auth_cb:
                    # No need to flatten and re-collect the args in
                    # handle_two_factor_auth
                    new_response = self.handle_two_factor_auth(args, kwargs)
                    new_response.history.append(response)
                    response = new_response
                if self._has_hit_abuse_detection(response):
                    self.handle_abuse_detection(response)
                elif self._has_hit_rate_limit(response):
                    __logs__.error(
                        'Status %d: %s', response.status_code, response.json())
                    self._fill_ratelimit_cache()
                    self._wait_for_ratelimit(resource=resource)
                else:
                    break
            except requests.exceptions.ConnectionError as e:
                __logs__.exception(e)
                __logs__.critical(
                    'Re-running request might lead to skipped '
                    'data. Do it anyway after %d seconds.',
                    self.DEFAULT_SLEEP_PERIOD)
                time.sleep(self.DEFAULT_SLEEP_PERIOD)
        self._cache_ratelimit_headers(response.headers, resource)
        return response

    def retrieve_client_credentials(self):
        """Return the client credentials.

        :returns: tuple(client_id, client_secret)
        """
        client_id = self.params.get('client_id')
        client_secret = self.params.get('client_secret')
        return (client_id, client_secret)

    def two_factor_auth_callback(self, callback):
        if not callback:
            return

        if not isinstance(callback, Callable):
            raise ValueError('Your callback should be callable')

        self.two_factor_auth_cb = callback

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
        # Unset username/password so we stop sending them
        self.auth = None

    @contextmanager
    def temporary_basic_auth(self, *auth):
        old_basic_auth = self.auth
        old_token_auth = self.headers.get('Authorization')

        self.basic_auth(*auth)
        yield

        self.auth = old_basic_auth
        if old_token_auth:
            self.headers['Authorization'] = old_token_auth

    @contextmanager
    def no_auth(self):
        """Unset authentication temporarily as a context manager."""
        old_basic_auth, self.auth = self.auth, None
        old_token_auth = self.headers.pop('Authorization', None)

        yield

        self.auth = old_basic_auth
        if old_token_auth:
            self.headers['Authorization'] = old_token_auth
