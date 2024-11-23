from core.libs.exceptions import MinorError

def test_minor_error_1():
    error = MinorError('Test message')
    assert error.message == 'Test message'
    assert error.status_code == 400

def test_minor_error_2():
    error = MinorError('Test message', 500)
    assert error.message == 'Test message'
    assert error.status_code == 500

def test_minor_error_dict():
    error = MinorError('Test message')
    assert error.to_dict() == {
        'message': 'Test message',
        'status_code': 400
    }



