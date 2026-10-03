from fastapi import APIRouter
from src.services.user import UserService
from src.schema.user import UserOutPutModel
from sqlalchemy import select, desc, or_, UUID
from pydantic import UUID4, EmailStr
from fastapi import Depends, Query
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.filter import UserFilters
from src.utils.auth import get_current_user_id
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/user-list")  # Сами создаем путя прямо тута и pycharm в них верит
async def get_user_list(filters: Annotated[UserFilters, Query()], user_id: UUID = Depends(get_current_user_id)) -> list[UserOutPutModel]:
    return [user.serialize() for user in await UserService.get_users_list(filters=filters)]

@router.get("/user-info")  # исправить путь
async def get_user_by_id(user_id: UUID = Depends(get_current_user_id)) -> UserOutPutModel:
    logger.debug(user_id)
    query_result = await UserService.get_user_by_id(user_id)
    return query_result.serialize()
