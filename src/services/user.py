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
    async def create_user(data: UserCreate) -> User:
        if await UserService.is_user_already_exist(data.email):
            raise HTTPException(status_code=400, detail="User already exists")
        data.password = get_password_hash(data.password)
        new_user = repository_container.user_repository().add_one(data)
        return new_user

    @staticmethod
    async def get_users_list(filters: Filters) -> List[User]:
        return repository_container.user_repository().get_list(filters=filters)

    @staticmethod
    async def get_user_by_id(id: UUID) -> User:
        user = repository_container.user_repository().get_one(id=id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")  # выкакать исключение, raise - исключение
        return user

    @staticmethod
    async def is_user_already_exist(email: EmailStr) -> bool:
        user = repository_container.user_repository().get_one(email=email)
        if not user:
            return False
        return True

    @staticmethod
    async def login(user: UserLogin, response: Response, session: AsyncSession) -> str:
        new_user = await authenticate_user(user.email, user.password, session)
        jwt_token_data: dict = {"id": new_user.id}
        jwt_token = create_access_token(jwt_token_data)
        response.set_cookie("access_token", jwt_token)
        return "успешный вход"

    @staticmethod
    async def logout(response: Response) -> str:
        response.delete_cookie("access_token")
        return "вы вышли из системы"