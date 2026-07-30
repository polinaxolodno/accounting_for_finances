from pydantic import BaseModel, Field, UUID4

class MoneyBoxOutPutModel(BaseModel):
    id: UUID4 = Field(discription='id')
    moneyboxname: str = Field(discription='name')
    userid: UUID4 = Field(discription='user_id', foreign_key='user.id')
    moneygoal: float = Field(discription='money_goal')
    moneybudget: float = Field(discription='money_budget')

class MoneyBoxCreate(BaseModel):
    moneyboxname: str = Field(discription='name')
    userid: UUID4 = Field(discription='user_id', foreign_key='user.id')
    moneygoal: float = Field(discription='money_goal')
    moneybudget: float = Field(discription='money_budget')