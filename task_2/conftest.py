import asyncio
import pytest

from db_connector import DataBaseSessionManager
from service import Base, UserDB

TEST_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
TEST_USER = {"username": "JohnDou", "email": "john@example.com", "password": "12345678"}

test_sessionmanager = DataBaseSessionManager(TEST_SQLALCHEMY_DATABASE_URL)


@pytest.fixture(scope="module", autouse=True)
def init_models_wrap():
    async def init_models():
        await test_sessionmanager.init_models(Base)
        async with test_sessionmanager.session() as session:
            current_user = UserDB(username=TEST_USER["username"], email=TEST_USER["email"],
                                  password=TEST_USER["password"])
            session.add(current_user)
            await session.commit()

    asyncio.run(init_models())
