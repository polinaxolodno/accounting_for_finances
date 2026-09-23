from src.schema.dailyBudget import DailyBudgetCreate, DailyBudgetOutPutModel
from src.db.session import AsyncSession
from src.models.dailyBudget import DailyBudget
from src.schema.filter import Filters
from sqlalchemy import or_, desc, Any, UUID, select
from pydantic import UUID4, EmailStr
from fastapi import HTTPException, Response
from src.utils.auth import get_password_hash, authenticate_user, create_access_token
from src.container.repository import repository_container


class DailyBudgetService:


    @staticmethod
    async def create_dailyBudget(data: DailyBudgetCreate) -> DailyBudget:
        new_dailyBudget = repository_container.dailyBudget_repository().add_one(data)
        return new_dailyBudget

    @staticmethod
    async def get_dailyBudget(user_id: UUID) -> User:
        dailyBudget = repository_container.dailyBudget_repository().get_one(user_id=user_id)
        if not dailyBudget:
            raise HTTPException(status_code=404, detail="User not found")  # выкакать исключение, raise - исключение
        return dailyBudget
