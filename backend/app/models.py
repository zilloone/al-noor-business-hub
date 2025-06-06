# app/models.py
from sqlmodel import SQLModel, Field
from pydantic import EmailStr


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    is_retailer: bool = Field(default=False)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    

class UserCreate(UserBase):
    password: str
    

class UserPublic(UserBase):
    id: int
    

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    payload: str


