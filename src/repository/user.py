from src.models.user import User
from src.utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):

    model = User


    async def get_list(self, filters: UserFilters) -> list[User]:
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
                        User.username.ilike(f'%{filters.search_str}%'),
                        User.email.ilike(f'%{filters.search_str}%'),
                    )
                )
            if filters.date_create_gte is not None:
                query = query.filter(
                    User.date_joined >= filters.date_create_gte
                )
            if filters.date_create_lte is not None:
                query = query.filter(
                    User.date_joined <= filters.date_create_lte
                )
            query_result = await session.execute(query)
            query_result = [row[0] for row in query_result.all()]
        return query_result

