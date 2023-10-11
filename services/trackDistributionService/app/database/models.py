from .database import db
from model.pymongo_model import SimpleModel


class AuthorDB(SimpleModel):
    collection = db.author


class AlbumDB(SimpleModel):
    collection = db.album


class TrackDB(SimpleModel):
    collection = db.track
