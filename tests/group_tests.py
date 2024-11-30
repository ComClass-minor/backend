import pytest

@pytest.fixture
def test_group_data():
    return {
            'name': 'testgroup',
            'feild': 'testfield',
            'min_requirement': 1,
            'creator_id': 'testuser123'
        }

# we need to login first to get the token
@pytest.mark.asyncio
async def test_auth_token(async_client , test_student_data , test_student_login_data):
    response1 = await async_client.post("/student/signup",json=test_student_data)
    response = await async_client.post("/student/signin",json=test_student_login_data)
    assert response.status_code == 200
    return response.json()["data"]["token"]

@pytest.mark.asyncio
async def test_create_group(async_client,test_student_data , test_student_login_data):
    response1 = await async_client.post("/student/signup", json=test_student_data)

    # Sign in
    response2 = await async_client.post("/student/signin", json=test_student_login_data)

    auth_token = response2.json().get("data", {}).get("token")
    assert auth_token, "Authentication token not found!"

    response = await async_client.post("/group/create_group",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            'name': 'testgroup',
            'feild': 'testfield',
            'min_requirement': 1,
            'creator_id': 'testuser123'
        }
    )
    print(f"Create Group Response: {response.status_code}, {response.json()}")

    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Group created successfully"



# @pytest.mark.asyncio
# async def test_join_group
