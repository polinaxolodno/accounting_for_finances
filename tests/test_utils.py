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
from src.utils.auth import create_access_token

password_hasher = PasswordHasher()

async def test_create_token():
    encode_jwt = create_access_token({"id":'sdghf987y98w34r0'})
    decode_jwt = jwt.decode(encode_jwt, settings.SECRET_KEY, algorithms=["HS256"])
    assert decode_jwt.get("id") == 'sdghf987y98w34r0'
    expire = decode_jwt.get("exp")
    expire_datetime = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    assert expire == expire_datetime