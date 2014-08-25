# -*- coding: utf-8 -*-
"""All exceptions for the github3 library."""


class GitHubError(Exception):

    """The base exception class."""

    def __init__(self, resp):
        super(GitHubError, self).__init__(resp)
        #: Response code that triggered the error
        self.response = resp
        self.code = resp.status_code
        self.errors = []
        try:
            error = resp.json()
            #: Message associated with the error
            self.msg = error.get('message')
            #: List of errors provided by GitHub
            if error.get('errors'):
                self.errors = error.get('errors')
        except:  # Amazon S3 error
            self.msg = resp.content or '[No message]'

    def __repr__(self):
        return '<GitHubError [{0}]>'.format(self.msg or self.code)

    def __str__(self):
        return '{0} {1}'.format(self.code, self.msg)

    @property
    def message(self):
        """The actual message returned by the API."""
        return self.msg


class AuthenticationFailed(GitHubError):

    """Exception class for 401 responses."""

    pass


class ForbiddenError(GitHubError):

    """Exception class for 403 responses."""

    pass


class NotFoundError(GitHubError):

    """Exception class for 404 responses."""

    pass


class InvalidRequestError(GitHubError):

    """Exception class for 422 responses."""

    pass


class ServerError(GitHubError):

    """Exception class for 5xx responses."""

    pass


error_classes = {
    401: AuthenticationFailed,
    403: ForbiddenError,
    404: NotFoundError,
    422: InvalidRequestError,
}


def error_for(response):
    """Return the appropriate initialized exception class for a response."""
    if 500 <= response.status_code < 600:
        return ServerError(response)
    klass = error_classes.get(response.status_code, GitHubError)
    return klass(response)
