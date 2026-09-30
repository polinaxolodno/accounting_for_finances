from fastapi import APIRouter
from src.services.moneyBox import MoneyBoxService
from src.schema.moneyBox import MoneyBoxOutPutModel
from sqlalchemy import select, desc, or_
from src.schema.moneyBox import MoneyBoxCreate
from fastapi import Depends
from src.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.filter import Filters
router = APIRouter()


@router.post("/moneybox")
async def create_moneybox(money_box: MoneyBoxCreate, session: AsyncSession = Depends(get_session)) -> MoneyBoxOutPutModel:
    new_moneybox = await MoneyBoxService.create_moneybox(money_box, session)
    return new_moneybox.serialize()




@router.get("/moneybox-list")
async def get_moneybox_list(filters: Filters, session: AsyncSession = Depends(get_session)) -> list[MoneyBoxOutPutModel]:
    query_result = await MoneyBoxService.get_moneybox_list(filters, session)
    return [moneybox.serialize() for moneybox in query_result]
