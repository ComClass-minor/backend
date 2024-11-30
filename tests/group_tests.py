from core.server import app
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from core import db

client = TestClient(app)

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


# we need to login first to get the token
@pytest.fixture
async def auth_token(async_client):
    response = await async_client.post("/student/signin",
        json={
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
    )
    assert response.status_code == 200
    return response.json()["data"]["token"]

@pytest.mark.asyncio
async def test_create_group(async_client, auth_token):
    response = await async_client.post("/group/create_group",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            'name': 'testgroup',
            'field': 'testfield',
            'min_requirement': 1,
            'creator_id': 'testcreator'
        }
    )
    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Group created successfully"
    db.groups.delete_many({"name": "testgroup"})
    db.students.delete_many({"email": "test@example.com"})