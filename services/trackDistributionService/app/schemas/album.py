from pydantic import BaseModel, Field
from typing import Optional


FAKE_ALBUM_INFO = {
    "date": "01.01.2021"
}


class AlbumBase(BaseModel):
    name: str = Field(title="Название трека")
    authorID: int = Field(title="Идентификатор исполнителя")
    featuringAuthorID: Optional[list] = Field(title="Идентификаторы других исполнителей")


class Album(AlbumBase):
    albumID: int = Field(title="Идентификатор трека")
    tracks: list = Field(title="Треки в альбоме")
    info: dict = Field(title="Информация о треке", default=FAKE_ALBUM_INFO)
