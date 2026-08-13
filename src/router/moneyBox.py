from fastapi import APIRouter
from src.schema.moneyBox import MoneyBoxOutPutModel
from sqlalchemy import String, Integer, UUID
from sqlalchemy import select, desc, or_
from src.schema.moneyBox import MoneyBoxCreate
from fastapi import Depends
from src.db.session import get_session
from src.models.moneyBox import MoneyBox
from sqlalchemy.ext.asyncio import AsyncSession
from src.schema.filter import Filters
router = APIRouter()


@router.post("/moneybox", tags=["moneybox"])
async def create_moneybox(moneyBox: MoneyBoxCreate, session: AsyncSession = Depends(get_session)) -> MoneyBoxOutPutModel:
    #новый_названиеКласса = Название_модели(столбец_БД(схема) = Экземпляр_Класса.Название_состояния(свойства класса), ...)
    new_moneybox = MoneyBox(**moneyBox.model_dump())
    session.add(new_moneybox)
    await session.commit() #Запись состояния БД
    return new_moneybox.serialize()


@router.get("/moneybox-list")
async def get_moneybox_list(filters: Filters, session: AsyncSession = Depends(get_session)) ->list[MoneyBoxOutPutModel]:
    query = select(MoneyBox) #query - необработанный результат запроса к Бд ("тело" запроса те текст запроса, а не результат)
    if filters.limit is not None and filters.limit >= 0: #Добавили к тексту запроса параметры
        query = query.limit(filters.limit)
    if filters.offset is not None and filters.offset >= 0:
        query = query.offset(filters.offset)
    if filters.order_by is not None:
        if filters.order_desc:
            query = query.order_by(desc(filters.order_by))
        else:
            query = query.order_by(filters.order_by)
    if filters.search_str is not None:
        query = query.filter(
            or_(
                MoneyBox.moneyboxname.ilike(f"%{filters.search_str}%"),
            )
        )
    query_result = await session.execute(query) #query_result - информация которую получилось вытащить с помощью запроса из БД
    return [moneybox.serialize() for moneybox in query_result.scalars().all()]