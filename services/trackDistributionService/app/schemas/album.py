from pydantic import BaseModel, Field
from typing import Optional


class AlbumBase(BaseModel):
    name: str = Field(title="Название трека")
    authorID: int = Field(title="Идентификатор исполнителя")
    featuringAuthorID: Optional[list] = Field(title="Идентификаторы других исполнителей")


class Album(AlbumBase):
    id: int = Field(title="Идентификатор трека")
    tracks: list = Field(title="Треки в альбоме")
    info: dict = Field(title="Информация о треке")
