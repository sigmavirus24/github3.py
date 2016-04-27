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
        return '<{0} [{1}]>'.format(self.__class__.__name__,
                                    self.msg or self.code)

    def __str__(self):
        return '{0} {1}'.format(self.code, self.msg)

    @property
    def message(self):
        """The actual message returned by the API."""
        return self.msg


class ResponseError(GitHubError):
    """The base exception for errors stemming from GitHub responses."""
    pass


class TransportError(GitHubError):
    """Catch-all exception for errors coming from Requests."""

    msg_format = 'An error occurred while making a request to GitHub: {0}'

    def __init__(self, exception):
        Exception.__init__(self, exception)
        self.exception = exception
        self.msg = self.msg_format.format(str(exception))

    def __str__(self):
        return '{0}: {1}'.format(type(self.exception), self.msg)


class ConnectionError(TransportError):
    """Exception for errors in connecting to or reading data from GitHub."""

    msg_format = 'A connection-level exception occurred: {0}'


class UnprocessableResponseBody(ResponseError):
    """Exception class for response objects that cannot be handled."""
    def __init__(self, message, body):
        Exception.__init__(self, message)
        self.body = body
        self.msg = message

    def __repr__(self):
        return '<{0} [{1}]>'.format('UnprocessableResponseBody', self.body)

    def __str__(self):
        return self.message


class BadRequest(ResponseError):
    """Exception class for 400 responses."""
    pass


class AuthenticationFailed(ResponseError):
    """Exception class for 401 responses.

    Possible reasons:

    - Need one time password (for two-factor authentication)
    - You are not authorized to access the resource
    """
    pass


class ForbiddenError(ResponseError):
    """Exception class for 403 responses.

    Possible reasons:

    - Too many requests (you've exceeded the ratelimit)
    - Too many login failures
    """
    pass


class NotFoundError(ResponseError):
    """Exception class for 404 responses."""
    pass


class MethodNotAllowed(ResponseError):
    """Exception class for 405 responses."""
    pass


class NotAcceptable(ResponseError):
    """Exception class for 406 responses."""
    pass


class UnprocessableEntity(ResponseError):
    """Exception class for 422 responses."""
    pass


class ClientError(ResponseError):
    """Catch-all for 400 responses that aren't specific errors."""
    pass


class ServerError(ResponseError):
    """Exception class for 5xx responses."""
    pass


class UnavailableForLegalReasons(ResponseError):
    """Exception class for 451 responses."""
    pass


error_classes = {
    400: BadRequest,
    401: AuthenticationFailed,
    403: ForbiddenError,
    404: NotFoundError,
    405: MethodNotAllowed,
    406: NotAcceptable,
    422: UnprocessableEntity,
    451: UnavailableForLegalReasons,
}


def error_for(response):
    """Return the appropriate initialized exception class for a response."""
    klass = error_classes.get(response.status_code)
    if klass is None:
        if 400 <= response.status_code < 500:
            klass = ClientError
        if 500 <= response.status_code < 600:
            klass = ServerError
    return klass(response)
