from .exceptions import MinorError


def base_assertion(error_code , message):
    raise MinorError(message, error_code)


def assert_not_found(value, message="Resource not found"):
    if not value:
        raise base_assertion(404, message)


def assert_auth(condition, message="Unauthorized"):
    if not condition:
        raise base_assertion(401, message)


def assert_bad_request(value, message="Bad request"):
    if not value:
        raise base_assertion(400, message)