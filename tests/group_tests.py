import pytest
from bson import ObjectId
from core import db

@pytest.fixture
def test_group_data():
    return {
            'name': 'testgroup',
            'feild': 'testfield',
            'min_requirement': 1,
            'creator_id': 'testuser123'
        }

@pytest.fixture
def test_student_data2():
    return {
        "user_id": "testuser12345",
        "name": "Test Student 2",
        "email": "test@examples.com",
        "password": "testpassword12345",
    }

@pytest.fixture
def test_student_login_data2():
    return {
        "email": "test@examples.com",
        "password": "testpassword12345"
    }

# we need to login first to get the token
@pytest.mark.asyncio
async def test_auth_token(async_client , test_student_data , test_student_login_data):
    response1 = await async_client.post("/student/signup",json=test_student_data)
    response = await async_client.post("/student/signin",json=test_student_login_data)
    assert response.status_code == 200
    return response.json()["data"]["token"]

@pytest.mark.asyncio
async def test_create_group(async_client,test_student_data , test_student_login_data , test_group_data):
    response1 = await async_client.post("/student/signup", json=test_student_data)

    # Sign in
    response2 = await async_client.post("/student/signin", json=test_student_login_data)

    auth_token = response2.json().get("data", {}).get("token")
    assert auth_token, "Authentication token not found!"

    response = await async_client.post("/group/create_group",
        headers={"Authorization": f"Bearer {auth_token}"},
        json=test_group_data
    )

    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Group created successfully"



@pytest.mark.asyncio
async def test_join_group(async_client,test_student_data , test_student_login_data,test_group_data , test_student_data2 , test_student_login_data2):
    response = await async_client.post("/student/signup", json=test_student_data)
    response = await async_client.post("/student/signin", json=test_student_login_data)
    auth_token = response.json().get("data", {}).get("token")
    assert auth_token, "Authentication token not found!"


    response = await async_client.post("/group/create_group", headers={"Authorization": f"Bearer {auth_token}"}, json=test_group_data)
    group_id = response.json()["data"]["group"]["id"]

    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Group created successfully"

    response = await async_client.post("/student/signup", json=test_student_data2)
    response = await async_client.post("/student/signin", json=test_student_login_data2)


    user_id = response.json()["data"]["student"]["user_id"]

    response = await async_client.post("/group/join_group", json={"group_id": group_id, "user_id": user_id})

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Joined group successfully"


@pytest.mark.asyncio
async def test_leave_group_member(async_client,test_student_data , test_student_login_data,test_group_data , test_student_data2 , test_student_login_data2):
    response = await async_client.post("/student/signup", json=test_student_data)
    response = await async_client.post("/student/signin", json=test_student_login_data)
    auth_token = response.json().get("data", {}).get("token")
    assert auth_token, "Authentication token not found!"


    response = await async_client.post("/group/create_group", headers={"Authorization": f"Bearer {auth_token}"}, json=test_group_data)
    group_id = response.json()["data"]["group"]["id"]

    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Group created successfully"

    response = await async_client.post("/student/signup", json=test_student_data2)
    response = await async_client.post("/student/signin", json=test_student_login_data2)


    user_id = response.json()["data"]["student"]["user_id"]

    response = await async_client.post("/group/join_group", json={"group_id": group_id, "user_id": user_id})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Joined group successfully"

    response = await async_client.post("/group/leave_group", json={"group_id": group_id, "user_id": user_id})

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Left group successfully"

@pytest.mark.asyncio
async def test_leave_group_creator(async_client,test_student_data , test_student_login_data,test_group_data):
    response = await async_client.post("/student/signup", json=test_student_data)
    response = await async_client.post("/student/signin", json=test_student_login_data)
    auth_token = response.json().get("data", {}).get("token")
    assert auth_token, "Authentication token not found!"

    response = await async_client.post("/group/create_group", headers={"Authorization": f"Bearer {auth_token}"}, json=test_group_data)
    group_id = response.json()["data"]["group"]["id"]

    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Group created successfully"

    response = await async_client.post("/group/leave_group", json={"group_id": group_id, "user_id": test_student_data["user_id"]})

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Left group successfully"