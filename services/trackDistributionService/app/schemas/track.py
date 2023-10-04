from pydantic import BaseModel, Field
from typing import Optional


class TrackBase(BaseModel):
    name: str = Field(title="Название трека")
    authorID: int = Field(title="Идентификатор исполнителя")
    featuringAuthorID: Optional[list] = Field(title="Идентификаторы других исполнителей")
    albumID: int = Field(title="Идентификатор альбома")


class Track(TrackBase):
    id: int = Field(title="Идентификатор трека")
    info: dict = Field(title="Информация о треке")
