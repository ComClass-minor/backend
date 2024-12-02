import pytest
from httpx import AsyncClient


@pytest.fixture
def test_blog_data(author_id: str = "testuser123") -> dict:
    return {
        "title": "test title",
        "content": "test content",
        "author_id": author_id,
    }

@pytest.mark.asyncio
async def test_create_blog(async_client : AsyncClient, test_student_data: dict, test_student_login_data: dict , test_blog_data: dict):
    response = await async_client.post("/student/signup", json=test_student_data)
    response = await async_client.post("/student/signin", json=test_student_login_data)
    auth_token = response.json().get("data", {}).get("token")
    assert auth_token, "Authentication token not found!"
    print(f"auth_token: {auth_token}")

    response = await async_client.post("/blog/create_blog", 
                                       headers={"Authorization": f"Bearer {auth_token}"}, 
                                       json=test_blog_data
                                       )

    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Blog created successfully"    