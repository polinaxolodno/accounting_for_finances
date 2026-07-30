from pydantic import BaseModel, Field, UUID4

class UserOutPutModel(BaseModel):
    id: UUID4 = Field(discription='id')
    username: str  = Field(discription='name')
    email: str  = Field(discription='email')
    password: str  = Field(discription='password')

class UserCreate(BaseModel):
    username: str = Field(discription='name')
    email: str = Field(discription='email')
    password: str = Field(discription='password')