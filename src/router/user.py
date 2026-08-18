from fastapi import APIRouter
from src.schema.user import UserOutPutModel
from sqlalchemy import select, desc, or_, UUID4
from src.schema.user import UserCreate
from fastapi import Depends
from src.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.filter import Filters
from src.services.user import UserService
router = APIRouter()


@router.post("/user", tags=["users"])  # путя не должны повторятся
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)) -> UserOutPutModel:
    new_user = UserService.create_user(user, session)
    return new_user.serialize()


@router.get("/user-list")  # Сами создаем путя прямо тута и pycharm в него верит
async def get_user_list(filters: Filters, session: AsyncSession = Depends(get_session)) -> list[UserOutPutModel]:
    query_result = UserService.get_users_list(filters, session)
    return [user.serialize() for user in query_result]


@router.get("/user/{id}", tags=["users"])  # исправить путь
async def get_user_by_id(id: UUID4, session: AsyncSession = Depends(get_session)) -> UserOutPutModel:
    query_result = UserService.get_user_by_id(id, session)
    return query_result.serialize()
