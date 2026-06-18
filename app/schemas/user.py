from pydantic import BaseModel, Field

class AuthModel(BaseModel):
    login: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    repeat_password: str = Field(min_length=8, max_length=128)

class UserLogin(BaseModel):
    login: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)

class InDbUser(BaseModel):
    id: str
    login: str
    hashed_password: str
    created_at: str