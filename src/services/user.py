from src.schema.user import UserCreate, UserOutPutModel
from src.db.session import AsyncSession
from src.models.user import User
from src.schema.filter import Filters
from sqlalchemy import or_, desc, Any, UUID, select
from pydantic import UUID4
from fastapi import HTTPException


class UserService:


    @staticmethod
    async def create_user(data: UserCreate, session: AsyncSession) -> User:
        new_user = User(**data.model_dump())
        session.add(new_user)
        await session.commit()
        return new_user

    @staticmethod
    async def get_users_list(filters: Filters, session: AsyncSession) -> List[UserOutPutModel]:
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
        return query_result.scalars().all()

    @staticmethod
    async def get_user_by_id(id: UUID4, session: AsyncSession) -> User:
        query = await session.execute(select(User).where(User.id == id))
        user = query.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")  # выкакать исключение, raise - исключение
        return user