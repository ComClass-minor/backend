import pytest
from core.apis.student.register import verify_password, create_jwt_token, pwd_context
import jwt
from datetime import datetime, timedelta
import os



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


class TestAuth:
    @pytest.mark.asyncio
    async def test_signup_success(self, async_client , test_student_data):
        response = await async_client.post( "/student/signup", json=test_student_data)
        print(response.json())
        assert response.status_code == 201
        data = response.json()['data']['student']
        assert 'id' in data
        assert data['email'] == 'test@example.com'

    @pytest.mark.asyncio
    async def test_signup_duplicate_email(self, async_client , test_student_data):
        response1 = await async_client.post( "/student/signup", json=test_student_data )
        response2 = await async_client.post( "/student/signup", json=test_student_data )
            
        print(response2.json())
        assert response2.status_code == 409

    
    # @pytest.mark.asyncio
    # async def test_signin_success(self, async_client, test_student_login_data):
    #     response = await async_client.post( "/student/signin", json=test_student_login_data )

    #     print(response.json())
    #     assert response.status_code == 200
    #     assert response.json()["status"] == "success"
    #     db_student = await db.students.find_one({"email": "test@example.com"})
        