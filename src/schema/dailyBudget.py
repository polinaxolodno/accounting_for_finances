from pydantic import BaseModel, Field, UUID4
from datetime import datetime


class DailyBudgetOutPutModel(BaseModel):
    id: UUID4 = Field(description='id')
    budget: float = Field(description='budget')
    date_end: datetime = Field(description='date_end')
    userid: UUID4 = Field(description='user_id', foreign_key='user.id')


class DailyBudgetCreate(BaseModel):
    budget: float = Field(description='budget')
    date_end: datetime = Field(description='date_end')
    userid: UUID4 = Field(description='user_id', foreign_key='user.id')
