import jwt  # библиотека для генерации jwt токенов
from datetime import datetime, timedelta, timezone
from src.config import Settings


def create_access_token(data: dict):
    to_encode = data.copy()
    expire =  datetime.now(timezone.utc) + timedelta(days=7)  # получаем текущее время + неделю жизни для токена
    to_encode.update({"exp": expire})  # добавляем наше время в словарь для токена
    encode_jwt = jwt.encode(to_encode, Settings.SECRET_KEY, algorithm="HS256")
    return encode_jwt

