import pytest
import jwt
from starlette.requests import Request
from fastapi import HTTPException
from datetime import datetime, timedelta

from src.utils.auth import *
from src.config import settings

def _make_token(payload: dict, key: str = settings.SECRET_KEY) -> str:
    return jwt.encode(payload, key, algorithm="HS256")

def _request_with_cookies(cookie: str | None) -> Request:
    headers = [(b"cookie", cookie.encode())] if cookie else []
    return Request({"type": "http", "headers": headers})

def test_password_hash_is_not_plane_text():
    hashed = get_password_hash("96r87o3679")
    assert hashed != "96r87o3679"
    assert hashed.startswith("$argon2")

def test_password_hash_verifies():
    hashed = get_password_hash("7696986efouih")
    assert verify_password("7696986efouih", hashed)
    assert not verify_password("7696986efou", hashed)

def test_same_password_different_hashes():
    assert get_password_hash("453456345") != get_password_hash("453456345")

@pytest.mark.parametrize("token", [
    "not-a-jwt",
    _make_token({"id": "hdsg", "exp": datetime.now(timezone.utc) + timedelta(days=7)}, key="x"*32),
    _make_token({"id": "hdsg", "exp": datetime.now(timezone.utc) - timedelta(days=7)}),
], ids=["мусор вместо токена", "неверный ключ", "истекший токен"])
def test_bad_token(token):
    with pytest.raises(HTTPException, match = "403: Invalid token") as status_code:
        get_token_if_valid(token)
    assert status_code.value.status_code == 403