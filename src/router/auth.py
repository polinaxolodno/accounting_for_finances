from fastapi import APIRouter
from src.services.user import UserService
from src.schema.user import UserOutPutModel
from sqlalchemy import select, desc, or_, UUID
from pydantic import UUID4
from src.schema.user import UserCreate, UserLogin
from fastapi import Depends, Response, HTTPException
from src.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/register")
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)) -> UserOutPutModel:
    user = await UserService.create_user(user, session)
    return user.serialize()

@router.post("/login")
async def login(user: UserLogin, response: Response, session: AsyncSession = Depends(get_session)) -> str:
    return await UserService.login(user, response, session)

@router.post("/logout")
async def logout(response: Response) -> str:
    return await UserService.logout(response)
