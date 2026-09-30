from src.schema.moneyBox import MoneyBoxCreate, MoneyBoxOutPutModel
from src.db.session import AsyncSession
from src.models.moneyBox import MoneyBox
from src.schema.filter import Filters
from sqlalchemy import or_, desc, Any, UUID, select
from fastapi import HTTPException
from typing import List
from src.container.repository import repository_container


class MoneyBoxService:


    @staticmethod
    async def create_moneybox(data: MoneyBoxCreate) -> MoneyBox:
        new_moneybox = await repository_container.moneybox_repository().add_one(data.model_dump())
        return new_moneybox

    @staticmethod
    async def get_moneybox_list(filters: Filters) -> List[MoneyBox]:
        return repository_container.moneybox_repository().get_list(filters=filters)