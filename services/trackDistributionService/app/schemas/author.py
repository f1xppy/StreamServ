from pydantic import BaseModel, Field
from typing import Optional


FAKE_AUTHOR_INFO = {
    "links": "https://vk.com/flxppy",
    "country": "Россия"
}


class AuthorBase(BaseModel):
    name: str = Field(title='Псевдоним исполнителя/название группы')
    description: Optional[str] = Field(title="Описание исполнителя/группы")


class Author(AuthorBase):
    authorID: int = Field(title="Идентификатор исполнителя")
    tracks: list = Field(title="Треки исполнителя/группы")
    albums: list = Field(title="Альбомы исполнителя/группы")
    info: dict = Field(title="Информация о исполнителе/группе", default=FAKE_AUTHOR_INFO)
