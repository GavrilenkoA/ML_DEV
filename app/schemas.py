from uuid import UUID
from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserAuth(BaseModel):
    username: str = Field(..., max_length=50, description="username")
    email: str = Field(..., max_length=50, description="user email")
    password: str = Field(..., max_length=100, description="user password")


class UserOut(BaseModel):
    id: UUID
    email: str


class SystemUser(UserOut):
    password: str