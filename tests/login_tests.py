from fastapi.testclient import TestClient
import pytest
from core.apis.student.register import verify_password, create_jwt_token, pwd_context
from core.server import app
import jwt
from datetime import datetime, timedelta
import os
from httpx import AsyncClient
from fastapi import status
from core import db

client = TestClient(app)
# client = AsyncClient(app=app, base_url="http://testserver")


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
    async with AsyncClient(app=app, base_url="http://test") as client:
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


class TestAuth:
    @pytest.mark.asyncio
    async def test_signup_success(self, async_client):
        response = await async_client.post(
            "/student/signup",
            json={
                'email': 'test@example.com',
                'name': 'Test Student',
                'password': 'testpassword123',
                'user_id': 'testuser123'
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()['data']['student']
        assert 'id' in data
        assert data['email'] == 'test@example.com'
        # we will remove this entry from the database
        # so that we can test the duplicate email case
        await db.students.delete_one({"email": "test@example.com"})
    
    @pytest.mark.asyncio
    async def test_db_cleanup(self, clean_db):
        """Test that database cleanup is working."""
        db = clean_db
        # Verify no test user exists
        user = await db.students.find_one({"email": "test@example.com"})
        assert user is None

    @pytest.mark.asyncio
    async def test_signup_duplicate_email(self, async_client):
        
        # Try duplicate signup
        response = await async_client.post(
            "/student/signup",
            json=test_student_data
        )
        assert response.status_code == status.HTTP_409_CONFLICT