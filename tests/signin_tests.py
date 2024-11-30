from core.server import app
from fastapi.testclient import TestClient
from httpx import AsyncClient
from fastapi import status
import pytest
from core import db

client = TestClient(app)

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

async def test_signin(async_client):
    response = await async_client.post("/student/signin",
            json={
                'email': 'test@example.com',
                'password': 'testpassword123'
            }
        )
    print(response.json())
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Student signed in successfully"
    # db.students.delete_many({"email": "test@example.com"})


async def test_incorrectpass_signup(async_client):
    response = await async_client.post("/student/signin",
            json={
                'email': 'test@example.com',
                'password': 'testpassword12'
            }
        )
    print(response.json())
    assert response.status_code == 401
    assert response.json()["status"] == "error"
    assert response.json()["message"] == "Invalid password"


async def test_notfound_signup(async_client):
    response = await async_client.post("/student/signin",
            json={
                'email': 'test@exampl.com',
                'password': 'testpassword123'
            }
        )
    print(response.json())
    assert response.status_code == 404
    assert response.json()["status"] == "error"
    assert response.json()["message"] == "Student not found"
    db.students.delete_many({"email": "test@example.com"})