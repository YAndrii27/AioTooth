class ApiException(BaseException):
    pass


class Forbidden(ApiException):
    pass


class Unauthorized(ApiException):
    pass


class NotFound(ApiException):
    pass


class UnprocessableEntity(ApiException):
    pass


class ServiceUnavailable(ApiException):
    pass


class UnmatchedApiVersion(ApiException):
    pass
