from random import randint

from .exceptions import BadRequest, InternalError, NotFound


def random_uint(limit: int) -> int:
    return randint(0, limit)


ERRORS_STATUS_CODE = {
    400: BadRequest,
    404: NotFound,
    500: InternalError,
}


def handle_requests_errors(response):
    if response.status_code in ERRORS_STATUS_CODE:
        raise ERRORS_STATUS_CODE[response.status_code](response.text)
