import jwt  # библиотека для генерации jwt токенов
from datetime import datetime, timedelta, timezone
from src.config import settings
from fastapi import HTTPException, Request, Depends
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from src.db.session import AsyncSession
from src.models.user import User
from pydantic import UUID4, EmailStr
from sqlalchemy import select, desc, or_, UUID

import logging

logger = logging.getLogger(__name__)

password_hasher = PasswordHasher()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire =  datetime.now(timezone.utc) + timedelta(days=7)  # получаем текущее время + неделю жизни для токена
    to_encode.update({"exp": expire})  # добавляем наше время в словарь для токена
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encode_jwt

def get_token_if_valid(token: str) -> dict:
    try:
        # payload - расшифрованный токен
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    # Входим если ошибка случилась
    except jwt.InvalidTokenError:
        raise HTTPException(403, "Invalid token")
    expire = payload.get("exp")
    expire_datetime = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire_datetime) or (expire_datetime < datetime.now(timezone.utc)):
        raise HTTPException(403, "Token is expired")
    return payload

def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(403, "Access Token is required")
    return token

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        password_hasher.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False

async def authenticate_user(email: str, password: str, session: AsyncSession ) -> User:
    query = await session.execute(select(User).where(User.email == email))
    user = query.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")  # выкакать исключение, raise - исключение
    if not verify_password(password, user.password):
        raise HTTPException(status_code=403, detail="Incorrect password")
    return user

def get_password_hash(password: str) -> str:
    return password_hasher.hash(password)

def get_user_id_from_token(token: str) -> UUID:
    logger.info(token)
    jwt_payload: dict = get_token_if_valid(token)
    user_id = jwt_payload.get("id")
    logger.info("Пиписька " + user_id)
    if not user_id:
        raise HTTPException(403, "Here is no email in jwt_token")
    return user_id

def get_current_user_id(token: str = Depends(get_token)) -> UUID:
    logger.debug(token)
    return get_user_id_from_token(token)
