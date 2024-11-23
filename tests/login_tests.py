from fastapi.testclient import TestClient
import pytest
from core.apis.student.register import verify_password, create_jwt_token, pwd_context
from core.server import app
import jwt
from datetime import datetime, timedelta
import os
import httpx

client = TestClient(app)
client = httpx.AsyncClient(app=app, base_url="http://testserver")


@pytest.fixture
def test_student_data():
    return {
        "user_id": "testuser123",
        "name": "Test Student",
        "email": "test@example.com",
        "password": "testpassword123",
    }

@pytest.fixture
def test_student_login_data():
    return {
        "email": "test@example.com",
        "password": "testpassword123"
    }

SECRET_KEY = os.getenv("SECRET_KEY")

@pytest.fixture
async def async_client():
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

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


# Asynchronous Test: Successful signup
@pytest.mark.asyncio
async def test_successful_signup(async_client, test_student_data):
    response = await async_client.post("/student/signup", json=test_student_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Student created successfully"
    assert "token" in data["data"]
    assert "student" in data["data"]
    assert data["data"]["student"]["email"] == test_student_data["email"]

# Asynchronous Test: Duplicate signup
@pytest.mark.asyncio
async def test_duplicate_signup(async_client, test_student_data):
    # Initial signup
    await async_client.post("/student/signup", json=test_student_data)

    # Duplicate signup
    response = await async_client.post("/student/signup", json=test_student_data)
    assert response.status_code == 409
    
    data = response.json()
    assert data["status"] == "error"
    assert data["message"] == "Email already in use"

    # Cleanup: Optional deletion logic
    # response = await async_client.delete(f"/student/{test_student_data['user_id']}")
    # assert response.status_code == 204