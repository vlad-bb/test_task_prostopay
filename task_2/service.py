import asyncio
import re
from datetime import date
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import DateTime, func, String, select
from sqlalchemy.orm import Mapped, mapped_column

from db_connector import sessionmanager, DeclarativeBase, AsyncSession


class Base(DeclarativeBase):
    """Base class for models"""
    created_at: Mapped[date] = mapped_column(
        "created_at", DateTime, default=func.now(), nullable=True
    )
    updated_at: Mapped[date] = mapped_column(
        "updated_at", DateTime, default=func.now(), onupdate=func.now(), nullable=True
    )


class UserDTO(BaseModel):
    """User data transfer object"""
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(max_length=50)
    password: str = Field(min_length=6, max_length=32)

    @field_validator('email')
    def email_validator(cls, value_email):
        """Email validator"""
        if re.search(r'[\w.-]+@[\w.-]+', value_email):
            return value_email
        raise ValueError("Invalid email")


class UserDB(Base):
    """User model"""
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)


class UserService:
    """Class for working with users"""

    def __init__(self, manager):
        self.session: AsyncSession | None = None
        self.sessionmanager = manager

    async def get_user_by_email(self, email: str) -> UserDB | None:
        """Get user by email"""
        async with self.sessionmanager.session() as self.session:
            stmt = select(UserDB).filter_by(email=email)
            user = await self.session.execute(stmt)
            user = user.scalar_one_or_none()
            return user

    async def get_user_by_id(self, user_id: int) -> UserDB | None:
        """Get user by id"""
        async with self.sessionmanager.session() as self.session:
            stmt = select(UserDB).filter_by(id=user_id)
            user = await self.session.execute(stmt)
            user = user.scalar_one_or_none()
            return user

    async def create_user(self, user: UserDTO) -> UserDB:
        """Create user from UserDTO object"""
        if await self.get_user_by_email(user.email):
            raise ValueError('User with this email already exists')
        async with self.sessionmanager.session() as self.session:
            user = UserDB(**user.model_dump())
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user


async def main():
    """Display the result of the work of the service class"""
    user_service = UserService(sessionmanager)  # Create user service object
    user_object = UserDTO(username='Bob', email='bob@gmail.com', password='qwerty')  # Create user pydentic object
    user_db = await user_service.create_user(user_object)  # Create user in database
    print(user_db)


if __name__ == '__main__':
    asyncio.run(sessionmanager.init_models(Base))  # Create tables
    asyncio.run(main())  # Run the main function
