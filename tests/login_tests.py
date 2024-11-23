from fastapi.testclient import TestClient
import pytest
from core.apis.student.register import verify_password, create_jwt_token, pwd_context
from core.server import app
import jwt
from datetime import datetime, timedelta
import os

client = TestClient(app)

@pytest.fixture
def test_student_data():
    return {
        "name": "Test Student",
        "email": "test@example.com",
        "password": "testpassword123",
        "created_at": str(datetime.now()),
        "updated_at": str(datetime.now()),
        "rating": 0,
        "group_list": [],
        "group_limit": 5
    }

@pytest.fixture
def test_student_login_data():
    return {
        "email": "test@example.com",
        "password": "testpassword123"
    }

SECRET_KEY = os.getenv("SECRET_KEY")

def test_verify_password():
    password = "testpassword123"
    hashed_password = pwd_context.hash(password)
    assert verify_password(password, hashed_password) == True
    assert verify_password("wrongpassword", hashed_password) == False


def test_create_jwt_token1():
    payload = {"email": "test@example.com"}
    token = create_jwt_token(payload)

    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    assert decoded["email"] == payload["email"]


def test_create_jwt_token2():
    payload = {"email": "test@example.com" , "exp": datetime.now() + timedelta(seconds=10)}
    token = create_jwt_token(payload, timedelta(minutes=10))

    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    assert "exp" in decoded

