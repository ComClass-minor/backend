import pytest



@pytest.mark.asyncio
async def test_signin(async_client , test_student_data , test_student_login_data):
    response1 = await async_client.post("/student/signup",json=test_student_data)
    response = await async_client.post("/student/signin",json=test_student_login_data)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Student signed in successfully"



async def test_incorrectpass_signup(async_client , test_student_data):
    res = await async_client.post("/student/signup", json=test_student_data)
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