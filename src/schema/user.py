from pydantic import BaseModel, Field, UUID4
from datetime import datetime

class UserOutPutModel(BaseModel):
    id: UUID4 = Field(description='id')
    username: str  = Field(description='name')
    email: str  = Field(description='email')
    date_joined: datetime = Field(description='date_joined')

class UserCreate(BaseModel):
    username: str = Field(description='name')
    email: str = Field(description='email')
    password: str = Field(description='password')
    date_joined: datetime = Field(description='date_joined')