from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import DeclarativeBase
from src.config import settings


engine: AsyncEngine = create_async_engine(url=settings.DB.SQLALCHEMY_DATABASE_URI_ASYNC, echo=True)
async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
