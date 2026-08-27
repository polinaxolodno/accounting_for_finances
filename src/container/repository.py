from src.repository.moneyBox import MoneyBoxRepository
from src.repository.user import UserRepository
from dataclasses import dataclass
from src.db.session import async_session_maker
from src.config import settings, Settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


@dataclass
class RepositoryContainer:

    async_session_maker: async_sessionmaker[AsyncSession]

    def user_repository(self) -> UserRepository:
        return UserRepository(async_session_maker=self.async_session_maker)

    def moneybox_repository(self) -> MoneyBoxRepository:
        return MoneyBoxRepository(async_session_maker=self.async_session_maker)


repository_container = RepositoryContainer(async_session_maker= async_session_maker)