from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy import select


class AbstractRepository(ABC):


    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def get_one():
        raise NotImplementedError

    @abstractmethod
    async def get_list():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):


    model = None

    def __init__(self, async_session_maker: AsyncSession):
        self.async_session_maker = async_session_maker

    async def add_one(self, data: dict):
        new_object = self.model(**data)
        # with - гарантирует что сессия закроетсся даже при ошибке
        async with self.async_session_maker() as session:
            session.add(new_object)
            await session.commit()
        return new_object

    async def get_one(self, **filter_by):
        async with self.async_session_maker() as session:
            query = select(self.model).filter_by(**filter_by)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
        return result

    async def get_list(self):
        async with self.async_session_maker() as session:
            query = select(self.model)
            query_result = await session.execute(query)
            query_result = [row[0] for row in query_result.all()]
        return query_result



