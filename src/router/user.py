from fastapi import APIRouter
from src.services.user import UserService
from src.schema.user import UserOutPutModel
from sqlalchemy import select, desc, or_, UUID
from pydantic import UUID4, EmailStr
from fastapi import Depends
from src.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.filter import Filters
from src.utils.auth import get_current_user_email

router = APIRouter()


@router.get("/user-list")  # Сами создаем путя прямо тута и pycharm в него верит
async def get_user_list(filters: Filters, user_email: EmailStr = Depends(get_current_user_email)) -> list[UserOutPutModel]:
    return [user.serialize() for user in await UserService.get_user_list(filters=filters)]

@router.get("/user-info")  # исправить путь
async def get_user_by_email(user_email: EmailStr = Depends(get_current_user_email), session: AsyncSession = Depends(get_session)) -> UserOutPutModel:
    query_result = await UserService.get_user_by_email(user_email, session)
    return query_result.serialize()
