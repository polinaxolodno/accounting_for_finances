from src.schema.dailyBudget import DailyBudgetCreate, DailyBudgetOutPutModel
from src.db.session import AsyncSession
from src.models.dailyBudget import DailyBudget
from sqlalchemy import or_, desc, Any, UUID, select
from pydantic import UUID4, EmailStr
from fastapi import HTTPException, Response
from datetime import date
from src.container.repository import repository_container


class DailyBudgetService:


    @staticmethod
    async def create_dailyBudget(data: DailyBudgetCreate) -> DailyBudget:
        delta=date(data.date_end)-date.today()
        data.daily_budget=data.total_budget/delta.days
        new_dailyBudget = repository_container.dailyBudget_repository().add_one(data)
        return new_dailyBudget

    @staticmethod
    async def get_dailyBudget(user_id: UUID, data: DailyBudgetOutPutModel) -> DailyBudget:
        dailyBudget = repository_container.dailyBudget_repository().get_one(user_id=user_id)
        delta=date(data.date_end)-date.today()
        data.daily_budget=data.total_budget/delta.days
        if not dailyBudget:
            raise HTTPException(status_code=404, detail="User not found")  # выкакать исключение, raise - исключение
        return dailyBudget
