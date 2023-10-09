from .schemas.author import Author, AuthorBase
from .schemas.track import Track
from .schemas.album import Album
from .database.models import AuthorDB, AlbumDB, TrackDB
from .database.database import db
from fastapi.responses import JSONResponse


def create_author(result: Author):
    commit = AuthorDB(result)
    commit.save()
    return result


def create_album(result: Album):
    author = db.author.find_one({"authorID": result.authorID}, {'_id': 0})
    if author != None:
        db.author.update_one({"authorID": result.authorID}, {'$push': {"albums": result.albumID}})
        for i in result.featuringAuthorID:
            author = db.author.find_one({"authorID": i}, {'_id': 0})
            if author != None:
                db.author.update_one({"authorID": i}, {'$push': {"albums": result.albumID}})
            else:
                return JSONResponse(status_code=404, content={"message": "Feat. author not found"})
        commit = AlbumDB(result)
        commit.save()
        return result
    return JSONResponse(status_code=404, content={"message": "Author not found"})

def create_track(result: Track):
    author = db.author.find_one({"authorID": result.authorID}, {'_id': 0})
    album = db.album.find_one({"albumID": result.albumID}, {'_id': 0})
    if author != None and album != None:
        db.author.update_one({"authorID": result.authorID}, {'$push': {"tracks": result.trackID}})
        db.album.update_one({"albumID": result.albumID}, {'$push': {"tracks": result.trackID}})
        for i in result.featuringAuthorID:
            author = db.author.find_one({"authorID": result.authorID}, {'_id': 0})
            if author != None:
                db.author.update_one({"authorID": i}, {'$push': {"tracks": result.trackID}})
            else:
                return JSONResponse(status_code=404, content={"message": "Feat. author not found"})
        commit = TrackDB(result)
        commit.save()
        return result
    if author == None:
        return JSONResponse(status_code=404, content={"message": "Author not found"})
    if album == None:
        return JSONResponse(status_code=404, content={"message": "Album not found"})


def get_authors():
    result = db.author.find()
    return result


def get_albums():
    return db.album.find()


def get_tracks():
    return db.track.find()


def get_author(ID:int):
    return db.author.find_one({"authorID": ID}, {'_id': 0})


def get_album(ID:int):
    return db.album.find_one({"albumID": ID}, {"_id":0})


def get_track(ID:int):
    return db.track.find_one({"trackID": ID}, {"_id": 0})

def update_author(ID:int, result:AuthorBase):
    author = db.author.find_one({"authorID": ID}, {'_id': 0})
    if author != None:
        db.author.update_one({"authorID": ID}, {"$set": {"name": result.name}})
        db.author.update_one({"authorID": ID}, {"$set": {"description": result.description}})
        return db.author.find_one({"authorID": ID}, {'_id': 0})

    return JSONResponse(status_code=404, content={"message": "Item not found"})


def update_album(ID:int, name: str):
    album = db.album.find_one({"albumID": ID}, {"_id": 0})
    if album != None:
        db.album.update_one({"albumID": ID}, {"$set": {"name": name}})
        return db.album.find_one({"albumID": ID}, {"_id": 0})

    return JSONResponse(status_code=404, content={"message": "Item not found"})


def update_track(ID: int, name: str):
    track = db.track.find_one({"trackID": ID}, {"_id": 0})
    if track != None:
        db.track.update_one({"trackID": ID}, {"$set": {"name": name}})
        return db.track.find_one({"trackID": ID}, {"_id": 0})
    return JSONResponse(status_code=404, content={"message": "Item not found"})


def delete_author(ID:int):
    author = db.author.find_one({"authorID": ID}, {'_id': 0})
    if author != None:
        db.author.delete_one({"authorID": ID})
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})

    return JSONResponse(status_code=404, content={"message": "Item not found"})


def delete_album(ID:int):
    album = db.album.find_one({"albumID": ID}, {"_id": 0})
    if album != None:
        db.album.delete_one({"albumID": ID})
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})

    return JSONResponse(status_code=404, content={"message": "Item not found"})


def delete_track(ID: int):
    track = db.track.find_one({"trackID": ID}, {"_id": 0})
    if track != None:
        db.track.delete_one({"trackID": ID})
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})
