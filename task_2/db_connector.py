import contextlib

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./dev.db"


class SessionException(Exception):
    """Exception raised for errors in the session."""
    pass


class DataBaseSessionManager:
    """Manage the database session."""

    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(autoflush=False, autocommit=False,
                                                                     bind=self._engine)

    async def init_models(self, Base: DeclarativeBase):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @contextlib.asynccontextmanager
    async def session(self):
        """Provide a transactional scope around a series of operations."""
        if self._session_maker is None:
            raise SessionException('Session is not initialized')
        session = self._session_maker()
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DataBaseSessionManager(SQLALCHEMY_DATABASE_URL)

