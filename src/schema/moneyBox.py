from pydantic import BaseModel, Field, UUID4

class MoneyBoxOutPutModel(BaseModel):
    id: UUID4 = Field(description='id')
    moneyboxname: str = Field(description='name')
    userid: UUID4 = Field(description='user_id', foreign_key='user.id')
    moneygoal: float = Field(description='money_goal')
    moneybudget: float = Field(description='money_budget')

class MoneyBoxCreate(BaseModel):
    moneyboxname: str = Field(description='name')
    userid: UUID4 = Field(description='user_id', foreign_key='user.id')
    moneygoal: float = Field(description='money_goal')
    moneybudget: float = Field(description='money_budget')