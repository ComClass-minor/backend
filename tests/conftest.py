# tests/conftest.py
import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from core.server import app
from core import db

# Configure pytest-asyncio
pytest_plugins = ('pytest_asyncio',)

client = TestClient(app)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def client():
    """Create a TestClient instance for synchronous testing."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
async def async_client():
    """Create an AsyncClient instance for asynchronous testing."""
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client


@pytest.fixture(autouse=True)
async def clean_db():
    """Clean up test data before and after tests."""
    # Clean up before test
    await db.students.delete_many({})
    await db.groups.delete_many({})
    await db.blogs.delete_many({})

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