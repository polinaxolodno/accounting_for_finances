from fastapi import APIRouter
from src.schema.user import UserOutPutModel
from sqlalchemy import String, Integer, UUID
from sqlalchemy import select
from src.schema.user import UserCreate
from fastapi import Depends
from src.db.session import get_session
from src.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter()


@router.post("/user", tags=["users"])
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)) -> UserOutPutModel:
    new_user = User(username=user.username, email=user.email, password=user.password)
    session.add(new_user)
    await session.commit()
    return new_user

@router.get("/user-list")#Сами создаем путя прямо тута и pycharm в него верит
async def get_user_list(session: AsyncSession = Depends(get_session)) -> list[UserOutPutModel]:
     query = await session.execute(select(User))
     users = query.scalars().all()
     return users



