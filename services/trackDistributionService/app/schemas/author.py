from pydantic import BaseModel, Field
from typing import Optional


class AuthorBase(BaseModel):
    name: str = Field(title='Псевдоним исполнителя/название группы')
    description: Optional[str] = Field(title="Описание исполнителя/группы")


class Author(AuthorBase):
    id: int = Field(title="Идентификатор исполнителя/группы")
    tracks: list = Field(title="Треки исполнителя/группы")
    info: dict = Field(title="Информация о исполнителе/группе")
