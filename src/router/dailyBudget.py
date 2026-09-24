from fastapi import APIRouter
from src.services.dailyBudget import DailyBudgetService
from src.schema.dailyBudget import DailyBudgetOutPutModel, DailyBudgetCreate
from sqlalchemy import select, desc, or_, UUID
from pydantic import UUID4
from fastapi import Depends
from src.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.filter import Filters
from src.utils.auth import get_current_user_id

router = APIRouter()


@router.post("/dailyBudget")
async def register(data: DailyBudgetCreate) -> DailyBudgetOutPutModel:
    new_dailyBudget = await DailyBudgetService.create_dailyBudget(data)
    return new_dailyBudget.serialize()

@router.get("/dayleBudget-info")
async def get_dailyBudget_by_user_id(user_id: UUID = Depends(get_current_user_id)) -> DailyBudgetOutPutModel:
    query_result = await DailyBudgetService.get_dailyBudget(user_id)
    return query_result.serialize()
