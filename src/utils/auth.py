import jwt  # библиотека для генерации jwt токенов
from datetime import datetime, timedelta, timezone
from src.config import Settings
from fastapi import HTTPException, Request
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from src.db.session import AsyncSession
from src.models.user import User

password_hasher = PasswordHasher()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire =  datetime.now(timezone.utc) + timedelta(days=7)  # получаем текущее время + неделю жизни для токена
    to_encode.update({"exp": expire})  # добавляем наше время в словарь для токена
    encode_jwt = jwt.encode(to_encode, Settings.SECRET_KEY, algorithm="HS256")
    return encode_jwt

def get_token_if_valid(token: str) -> dict:
    try:
        # payload - расшифрованный токен
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=["HS256"])
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