from pydantic import BaseModel, Field

class AuthModel(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    repeat_password: str = Field(min_length=8, max_length=128)

class UserPublic(BaseModel):
    id: str
    username: str
    created_at: str


class UserLogin(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)

class InDbUser(BaseModel):
    id: str
    username: str
    hashed_password: str
    created_at: str