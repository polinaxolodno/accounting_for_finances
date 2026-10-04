from src.schema.dailyBudget import DailyBudgetCreate
from src.models.dailyBudget import DailyBudget
from sqlalchemy import or_, desc, Any, UUID, select
from pydantic import UUID4, EmailStr
from fastapi import HTTPException, Response
from datetime import date
from src.container.repository import repository_container


def days_left(date_end: datatime) -> int:
    return (date_end.date() - date.today()).days


class DailyBudgetService:


    @staticmethod
    async def create_dailyBudget(data: DailyBudgetCreate) -> DailyBudget:
        if await repository_container.dailyBudget_repository().get_one(userid=data.userid):
            raise HTTPException(status_code = 400, detail = "У пользователя есть ежедневный бюджет. НЕ может быть больше 1")
        delta = days_left(data.date_end)
        if delta < 1:
            raise HTTPException(status_code = 400, detail = "Дата за периодом")
        new_data = data.model_dump()
        new_data["daily_budget"] = data.total_budget/delta
        new_daily_budget = await repository_container.dailyBudget_repository().add_one(new_data)
        return new_daily_budget

    @staticmethod
    async def get_dailyBudget(user_id: UUID) -> DailyBudget:
        dailyBudget = await repository_container.dailyBudget_repository().get_one(userid=user_id)
        if not dailyBudget:
            raise HTTPException(status_code = 404, detail = "У пользователя нет бюджета")
        delta = days_left(data.date_end)
        if delta < 1:
            raise HTTPException(status_code = 400, detail = f"Период кончился. Остаток: {total_budget}")
        daily_budget.daily_budget = data.total_budget/delta
        return daily_budget
