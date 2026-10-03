from src.models.moneyBox import MoneyBox
from src.utils.repository import SQLAlchemyRepository


class MoneyBoxRepository(SQLAlchemyRepository):
    
    model = MoneyBox


    async def get_list(self, filters: MoneyBoxFilter) -> list[MoneyBox]:
        async with self.async_session_maker() as session:
            query = select(self.model)
            if filters.limit is not None and filters.limit >= 0:
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
                    MoneyBox.moneyboxname.ilike(f'%{filters.search_str}%')
                    )
            )
        query_result = await session.execute(query)
        query_result = [row[0] for row in query_result.all()]
        return query_result
