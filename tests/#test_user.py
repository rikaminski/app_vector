import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.database import get_db
from app.main import app

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(base_url="http://localhost:8009") as ac:
        yield ac

@pytest_asyncio.fixture
async def db_session():
    async for session in get_db():
        yield session

@pytest.mark.asyncio
async def test_create_user(async_client: AsyncClient, db_session: AsyncSession):
    user_data = {
        "name": "Test User",
        "nickname": "testuser",
        "email": "testuser2@example.com",
        "password": "password123",
        "confirm_password": "password123"
    }
    response = await async_client.post("/user/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["nickname"] == user_data["nickname"]
    assert data["email"] == user_data["email"]

    user_in_db = await db_session.execute(
        db_session.query(User).filter(User.email == user_data["email"])
    )
    user = user_in_db.scalar_one_or_none()
    assert user is not None
    assert user.name == user_data["name"]
    assert user.nickname == user_data["nickname"]
    assert user.email == user_data["email"]
