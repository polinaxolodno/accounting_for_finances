from src.schema.user import UserCreate, UserLogin
from src.models.user import User
from src.schema.filter import UserFilter
from sqlalchemy import or_, desc, Any, UUID, select
from pydantic import UUID4, EmailStr
from fastapi import HTTPException, Response
from src.utils.auth import get_password_hash, authenticate_user, create_access_token
from typing import List
from src.container.repository import repository_container
import logging


logger = logging.getLogger(__name__)

class UserService:


    @staticmethod
    async def create_user(data: UserCreate) -> User:
        logger.debug(f"Инфа при проверке: {await UserService.is_user_already_exist(data.email)}")
        if await UserService.is_user_already_exist(data.email):
            raise HTTPException(status_code=400, detail="User already exists")
        data.password = get_password_hash(data.password)
        new_user = await repository_container.user_repository().add_one(data.model_dump())
        return new_user

    @staticmethod
    async def get_users_list(filters: UserFilter) -> List[User]:
        return await repository_container.user_repository().get_list(filters=filters)

    @staticmethod
    async def get_user_by_id(id: UUID) -> User:
        logger.debug(id)
        user = await repository_container.user_repository().get_one(id=id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")  # выкакать исключение, raise - исключение
        return user

    @staticmethod
    async def is_user_already_exist(email: EmailStr) -> bool:
        user = await repository_container.user_repository().get_one(email=email)
        if user is None:
            return False
        return True

    @staticmethod
    async def login(user: UserLogin, response: Response, session: AsyncSession) -> str:
        new_user = await authenticate_user(user.email, user.password, session)
        logger.info(new_user)
        jwt_token_data: dict = {"id": str(new_user.id)}
        jwt_token = create_access_token(jwt_token_data)
        response.set_cookie("access_token", jwt_token)
        return "успешный вход"

    @staticmethod
    async def logout(response: Response) -> str:
        response.delete_cookie("access_token")
        return "вы вышли из системы"