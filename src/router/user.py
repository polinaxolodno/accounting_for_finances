from fastapi import APIRouter
from src.schema.user import UserOutPutModel
from sqlalchemy import String, Integer, UUID
from sqlalchemy import select, desc, or_
from src.schema.user import UserCreate
from fastapi import Depends
from src.db.session import get_session
from src.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.filter import Filters
router = APIRouter()

@router.post("/user", tags=["users"])
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)) -> UserOutPutModel:
    new_user = User(**user.model_dump())
    session.add(new_user)
    await session.commit()
    return new_user.serialize()

@router.post("/user-list")#Сами создаем путя прямо тута и pycharm в него верит
async def get_user_list(filters: Filters, session: AsyncSession = Depends(get_session)) -> list[UserOutPutModel]:
     query = select(User)
     if filters.limit is not None and filters.limit >= 0:
         query = query.limit(filters.limit)
     if filters.offset is not None and filters.offset >= 0:
         query = query.offset(filters.offset)
     if filters.order_by is not None:
         if filters.order_desc:
             query = query.order_by(desc(filters.order_by))
         else:
             query = query.order_by(filters.order_by)
     if filters.search_str is not None:
         query = query.filter(
             or_(
                 User.username.ilike(f'%{filters.search_str}%'),
                 User.email.ilike(f'%{filters.search_str}%'),
             )
         )
     query_result = await session.execute(query)
     return [user.serialize() for user in query_result.scalars().all()]



