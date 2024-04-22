import unittest
import asyncio
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.ext.asyncio import AsyncSession

from service import UserDB, UserService, UserDTO
from conftest import test_sessionmanager


class TestAsyncUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        """Set up the test case"""
        self.user = UserDB(id=1, username="test_user", password="test_password", email="test@email.com")
        self.session = AsyncMock(spec=AsyncSession)
        self.user_service = UserService(test_sessionmanager)

    async def test_get_user_by_email(self):
        """Test get user by email"""
        email = "test@email.com"
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = self.user
        self.session.execute.return_value = mocked_user
        result = await self.user_service.get_user_by_email(email)
        self.assertEqual(result.email, self.user.email)

    async def test_get_user_by_nonexistent_email(self):
        """Test get user by nonexistent email"""
        email = "nonexistent@email.com"
        result = await self.user_service.get_user_by_email(email)
        self.assertIsNone(result)

    async def test_get_user_by_id(self):
        """Test get user by id"""
        user_id = 1
        self.user_service.get_user_by_id = AsyncMock(return_value=self.user)
        result = await self.user_service.get_user_by_id(user_id)
        self.assertEqual(result.id, user_id)

    async def test_get_user_by_nonexistent_id(self):
        """Test get user by nonexistent id"""
        nonexistent_id = 999
        self.user_service.get_user_by_id = AsyncMock(return_value=None)
        result = await self.user_service.get_user_by_id(nonexistent_id)
        self.assertIsNone(result)

    async def test_create_user(self):
        """Test create user"""
        body = UserDTO(username="test_user", password="password", email="test@email.com")
        result = await self.user_service.create_user(body)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.password, body.password)
        self.assertEqual(result.email, body.email)

    async def test_create_user_existing_email(self):
        """Test create user with existing email"""
        existing_user = UserDB(id=2, username="existing_user", password="existing_password", email="existing@email.com")
        self.user_service.get_user_by_email = AsyncMock(return_value=existing_user)
        body = UserDTO(username="test_user", password="password", email="existing@email.com")
        with self.assertRaises(ValueError):
            await self.user_service.create_user(body)
