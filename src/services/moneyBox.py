from src.schema.moneyBox import MoneyBoxCreate
from src.models.moneyBox import MoneyBox
from src.schema.filter import MoneyBoxFilter
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
    async def get_moneybox_list(filters: MoneyBoxFilter) -> List[MoneyBox]:
        return await repository_container.moneybox_repository().get_list(filters=filters)