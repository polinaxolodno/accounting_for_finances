from src.schema.user import UserCreate, UserOutPutModel, UserLogin
from src.db.session import AsyncSession
from src.models.user import User
from src.schema.filter import Filters
from sqlalchemy import or_, desc, Any, UUID, select
from pydantic import UUID4, EmailStr
from fastapi import HTTPException, Response
from src.utils.auth import get_password_hash, authenticate_user, create_access_token
from typing import List
from src.container.repository import repository_container


class UserService:


    @staticmethod
    async def create_user(data: UserCreate, session: AsyncSession) -> User:
        if await UserService.is_user_already_exist(data.email, session):
            raise HTTPException(status_code=400, detail="User already exists")
        new_user = User(**data.model_dump(exclude_unset=True))  # model_dump - превращает схему в модель
        new_user.password = get_password_hash(new_user.password)
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
    async def get_user_by_email(email: EmailStr) -> User:
        user = repository_container.user_repository().get_one(email=email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")  # выкакать исключение, raise - исключение
        return user

    @staticmethod
    async def is_user_already_exist(email: EmailStr, session: AsyncSession) -> bool:
        query = await session.execute(select(User).where(User.email == email))
        user = query.scalar_one_or_none()
        if not user:
            return False
        return True

    @staticmethod
    async def login(user: UserLogin, response: Response, session: AsyncSession) -> str:
        await authenticate_user(user.email, user.password, session)
        jwt_token_data: dict = {"email": user.email}
        jwt_token = create_access_token(jwt_token_data)
        response.set_cookie("access_token", jwt_token)
        return "успешный вход"

    @staticmethod
    async def logout(response: Response) -> str:
        response.delete_cookie("access_token")
        return "вы вышли из системы"