from fastapi import APIRouter
from src.schema.user import UserOutPutModel
from sqlalchemy import select, desc, or_, UUID4
from src.schema.user import UserCreate
from fastapi import Depends, HTTPException
from src.db.session import get_session
from src.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.filter import Filters
router = APIRouter()


@router.post("/user", tags=["users"])  # путя не должны повторятся
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)) -> UserOutPutModel:
    new_user = User(**user.model_dump())
    session.add(new_user)
    await session.commit()
    return new_user.serialize()


@router.get("/user-list")  # Сами создаем путя прямо тута и pycharm в него верит
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
    if filters.date_create_gte is not None:
        query = query.filter(
            User.date_joined >= filters.date_create_gte
        )
    if filters.date_create_lte is not None:
        query = query.filter(
            User.date_joined <= filters.date_create_lte
        )
    query_result = await session.execute(query)
    return [user.serialize() for user in query_result.scalars().all()]


@router.get("/user/{id}", tags=["users"])  # исправить путь
async def get_user_by_id(id: UUID4, session: AsyncSession = Depends(get_session)) -> UserOutPutModel:
    query = select(User).filter(User.id == id).one_or_none()
    if query is None:
        raise HTTPException(status_code=404, detail="User not found")  # выкакать исключение, raise - исключение
    query_result = await session.execute(query)
    return query_result.scalars().one_or_none().serialize()
