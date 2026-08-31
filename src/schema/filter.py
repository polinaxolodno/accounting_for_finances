from pydantic import BaseModel, Field
from datetime import datetime


class Filters(BaseModel):
    limit: int | None = Field(description='limit', default=10)
    offset: int | None = Field(description='offset', default=0)
    order_desc: bool | None = Field(description='orderdesc', default=True)
    search_str: str | None = Field(description='search_str', default=None)
    # дата человеком вводится
    date_create_gte: datetime | None = Field(description='date_create_gte', default=None)  # больше или равно
    date_create_lte: datetime | None = Field(description='date_create_lte', default=None)  # меньше или равно


class UserFilter(Filters):
    order_by: str | None = Field(description='orderby', default='username')


class MoneyBoxFilter(Filters):
    order_by: str | None = Field(description='orderby', default='moneyboxname')