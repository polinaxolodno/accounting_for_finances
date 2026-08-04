from fastapi import APIRouter

from src.schema.moneyBox import MoneyBoxOutPutModel
from sqlalchemy import String, Integer, UUID
from sqlalchemy import select
from src.schema.moneyBox import MoneyBoxCreate
from fastapi import Depends
from src.db.session import get_session
from src.models.moneyBox import MoneyBox
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter()

@router.post("/moneybox", tags=["moneybox"])
async def create_moneybox(moneyBox: MoneyBoxCreate, session: AsyncSession = Depends(get_session)) -> MoneyBoxOutPutModel:
    #новый_названиеКласса = Название_модели(столбец_БД(схема) = Экземпляр_Класса.Название_состояния(свойства класса), ...)
    new_moneybox = MoneyBox(**moneyBox.model_dump())
    session.add(new_moneybox)
    await session.commit() #Запись состояния БД
    return new_moneybox.serialize()

@router.get("/moneybox-list")
async def get_moneybox_list(session: AsyncSession = Depends(get_session)) ->list[MoneyBoxOutPutModel]:
    query = await session.execute(select(MoneyBox)) #query - необработанный результат запроса к Бд
    return [moneybox.serialize() for moneybox in query.scalars().all()]