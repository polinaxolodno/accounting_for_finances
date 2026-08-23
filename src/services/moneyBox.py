from src.schema.moneyBox import MoneyBoxCreate, MoneyBoxOutPutModel
from src.db.session import AsyncSession
from src.models.moneyBox import MoneyBox
from src.schema.filter import Filters
from sqlalchemy import or_, desc, Any, UUID, select
from fastapi import HTTPException


class MoneyBoxService:


    @staticmethod
    async def create_moneybox(data: MoneyBoxCreate, session: AsyncSession) -> MoneyBox:
        # новый_названиеКласса = Название_модели(столбец_БД(схема) = Экз_Класса.Название_состояния(свойства класса), ...)
        new_moneybox = MoneyBox(**data.model_dump())
        session.add(new_moneybox)
        await session.commit()  # Запись состояния БД
        return new_moneybox

    @staticmethod
    async def get_moneybox_list(filters: Filters, session: AsyncSession) -> list[MoneyBoxOutPutModel]:
        query = select(MoneyBox)
        # query - необраб результат запроса к Бд ("тело" запроса те текст запроса, а не результат)
        if filters.limit is not None and filters.limit >= 0:  # Добавили к тексту запроса параметры
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
        query_result = await session.execute(query)
        # query_result - информация, которую получилось вытащить с помощью запроса из БД
        return query_result.scalars().all()