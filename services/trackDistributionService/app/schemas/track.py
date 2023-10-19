from pydantic import BaseModel, Field
from typing import Optional


FAKE_TRACK_INFO = {
    "date": "01.01.2021",
    "label": "xxx"
}


class TrackBase(BaseModel):
    name: str = Field(title="Название трека")
    authorID: int = Field(title="Идентификатор исполнителя")
    featuringAuthorID: Optional[list[int]] = Field(title="Идентификаторы других исполнителей")
    albumID: int = Field(title="Идентификатор альбома")


class Track(TrackBase):
    trackID: int = Field(title="Идентификатор трека")
    info: dict = Field(title="Информация о треке", default=FAKE_TRACK_INFO)
