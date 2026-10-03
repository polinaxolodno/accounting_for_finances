from pydantic import BaseModel, Field, UUID4
from datetime import datetime


class DailyBudgetOutPutModel(BaseModel):
    id: UUID4 = Field(description='id')
    total_budget: float = Field(description='total_budget')
    date_end: datetime = Field(description='date_end')
    daily_budget: float = Field(description='daily_budget')
    userid: UUID4 = Field(description='user_id', foreign_key='user.id')


class DailyBudgetCreate(BaseModel):
    total_budget: float = Field(description='total_budget')
    date_end: datetime = Field(description='date_end')
    userid: UUID4 = Field(description='user_id', foreign_key='user.id')
