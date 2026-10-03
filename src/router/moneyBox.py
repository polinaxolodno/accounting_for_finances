from fastapi import APIRouter
from src.services.moneyBox import MoneyBoxService
from src.schema.moneyBox import MoneyBoxOutPutModel
from sqlalchemy import select, desc, or_
from src.schema.moneyBox import MoneyBoxCreate
from fastapi import Depends, Query
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.filter import MoneyBoxFilter
router = APIRouter()


@router.post("/moneybox")
async def create_moneybox(money_box: MoneyBoxCreate) -> MoneyBoxOutPutModel:
    new_moneybox = await MoneyBoxService.create_moneybox(money_box)
    return new_moneybox.serialize()

@router.get("/moneybox-list")
async def get_moneybox_list(filters: Annotated[MoneyBoxFilter, Query()])-> list[MoneyBoxOutPutModel]:
    query_result = await MoneyBoxService.get_moneybox_list(filters)
    return [moneybox.serialize() for moneybox in query_result]
