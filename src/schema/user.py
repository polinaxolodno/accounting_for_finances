from pydantic import BaseModel, Field, UUID4

class UserOutPutModel(BaseModel):
    id: UUID4 = Field(description='id')
    username: str  = Field(description='name')
    email: str  = Field(description='email')

class UserCreate(BaseModel):
    username: str = Field(description='name')
    email: str = Field(description='email')
    password: str = Field(description='password')