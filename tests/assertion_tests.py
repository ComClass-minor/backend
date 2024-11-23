from core.libs import assertions
from core.libs.exceptions import MinorError

def test_base_assertion():
    try:
        assertions.base_assertion(404, "Resource not found")
    except MinorError as e:
        assert e.status_code == 404
        assert e.message == "Resource not found"

def test_assert_not_found():
    try:
        assertions.assert_not_found(False)
    except MinorError as e:
        assert e.status_code == 404
        assert e.message == "Resource not found"

def test_assert_auth():
    try:
        assertions.assert_auth(False)
    except MinorError as e:
        assert e.status_code == 401
        assert e.message == "Unauthorized"

def test_assert_bad_request():
    try:
        assertions.assert_bad_request(False)
    except MinorError as e:
        assert e.status_code == 400
        assert e.message == "Bad request"
