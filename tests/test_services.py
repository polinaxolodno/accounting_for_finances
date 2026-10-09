from src.schema.dailyBudget import DailyBudgetCreate
from src.models.dailyBudget import DailyBudget
from sqlalchemy import or_, desc, Any, UUID, select
from pydantic import UUID4, EmailStr
from fastapi import HTTPException, Response
from datetime import date
from src.container.repository import repository_container
from src.schema.moneyBox import MoneyBoxCreate
from src.models.moneyBox import MoneyBox
from src.schema.filter import MoneyBoxFilter
from typing import List
from src.schema.user import UserCreate, UserLogin
from src.models.user import User
from src.schema.filter import UserFilter
from src.utils.auth import get_password_hash, authenticate_user, create_access_token, verify_password
import logging
import pytest
from src.services.user import UserService


async def test_hash_password():
    user = await UserService.create_user(UserCreate(username = 'pol343', email = '113853@gmail.com', password ='78890'))
    assert user.password != "78890"
    assert verify_password('78890', user.password)

# Моя гениальная мысль привела меня к тому что
# мы вызвали функцию и должны проверить оба варианта, которые она возвращает
# и для этого нам не нужна переменная, а только assert True или False
# в целом я хз есть ли смысл такое проверять
# или тесты пишутся буквально для всего чтобы не тестить вручную на свагере
async def test_is_user_alredy_exist():
    result = await UserService.is_user_already_exist(email='11@gmail.com')
    assert result is True
    # Почему-то тест с ошибкой хотя почта это максимально рандомный набор символов
    result = await UserService.is_user_already_exist(email='6634r35t3t6@gmail.com')
    assert result is False

