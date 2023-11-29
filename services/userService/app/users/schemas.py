import uuid
from fastapi_users import schemas
from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True


class GroupRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class GroupUpsert(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class GroupUpdate(BaseModel):
    name: str

    class Config:
        orm_mode = True

        
class UserRead(schemas.BaseUser[uuid.UUID]):
    nickname: str | None = None
    real_name: str | None = None
    age: int | None = None
    group_id: int | None = None
    #geopos: str | None = "POINT (0 0)"


class UserCreate(schemas.BaseUserCreate):
    nickname: str | None = None
    real_name: str | None = None
    age: int | None = None
    group_id: int | None = None
    geopos: str | None = "POINT (0 0)"


class UserUpdate(schemas.BaseUserUpdate):
    nickname: str | None = None
    real_name: str | None = None
    age: int | None = None
    group_id: int | None = None
    