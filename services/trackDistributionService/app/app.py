import pymongo
from fastapi import FastAPI, UploadFile, File, Depends, Body
from fastapi.responses import JSONResponse
import json

from .schemas.author import Author, AuthorBase
from .schemas.track import Track, TrackBase
from .schemas.album import Album, AlbumBase
import typing
from . import crud
from .database.database import db


app = FastAPI(
    version="0.1", title="Track Distribution Service"
)


@app.post(
    "/authors", status_code=201, response_model=Author,
    summary="Добавляет исполнителя в базу"
)
async def add_author(author: AuthorBase):
    authorId = db.author.count_documents({}) + 1
    while True:
        _author = db.author.find_one({"authorID": authorId}, {'_id': 0})
        if _author == None:
           break
        authorId += 1
    result = Author(**author.dict(), tracks=[], albums=[], authorID=authorId)
    return crud.create_author(result)


@app.post(
    "/albums", status_code=202, response_model=Album, summary="Добавляет альбом в базу"
)
async def add_album(album: AlbumBase):
    albumId = db.album.count_documents({}) + 1
    while True:
        _album = db.album.find_one({"albumID": albumId}, {'_id': 0})
        if _album == None:
            break
        albumId += 1
    result = Album(**album.dict(), tracks=[], albumID=albumId)
    return crud.create_album(result)


@app.post(
    "/tracks", status_code=203, response_model=Track, summary="Добавляет трек в базу"
)
async def add_track(file: UploadFile, track=Body()):
    track = TrackBase(**json.loads(track))

    _track = db.track.find_one(sort=[("trackID", -1)])
    if _track == None:
        trackId = 1
    else:
        trackId = int(_track["trackID"])+1
    result = Track(**track.dict(), trackID=trackId)
    crud.upload_track_file(file, result.trackID)
    return crud.create_track(result)


@app.get(
    "/authors", summary="Возвращает список исполнителей", response_model=list[Author]
)
async def get_authors_list():
    return crud.get_authors()


@app.get(
    "/albums", summary="Возвращает список альбомов", response_model=list[Album]
)
async def get_albums_list() -> typing.Iterable[Album]:
    return crud.get_albums()


@app.get(
    "/tracks", summary="Возвращает список треков", response_model=list[Track]
)
async def get_tracks_list() -> typing.Iterable[Track]:
    return crud.get_tracks()


@app.get(
    "/authors/{authorId}", summary="Возвращает информацию о конкретном исполнителе"
)
async def get_author_info(authorId: int):
    author = crud.get_author(authorId)
    if author != None:
        return author
    return JSONResponse(status_code=404, content={"message": "Item not found"})


@app.get(
    "/albums/{albumId}", summary="Возвращает информацию о конкретном альбоме"
)
async def get_album_info(albumId: int):
    album = crud.get_album(albumId)
    if album != None:
        return album
    return JSONResponse(status_code=404, content={"message": "Item not found"})


@app.get(
    "/tracks/{trackId}", summary="Возвращает информацию о конкретном треке"
)
async def get_track_info(trackId: int):
    track = crud.get_track(trackId)
    if track != None:
        return track
    return JSONResponse(status_code=404, content={"message": "Item not found"})


@app.put(
    "/authors/{authorId}", summary="Обновляет информацию об исполнителе"
)
async def update_author(authorId: int, author: AuthorBase):
    result = AuthorBase(**author.dict())
    return crud.update_author(authorId, result)


@app.put(
    "/albums/{albumId}", summary="Добавляет альбом в базу"
)
async def update_album(albumId: int, name: str):
    return crud.update_album(albumId, name)


@app.put(
    "/tracks/{trackId}", summary="Добавляет трек в базу"
)
async def update_track(trackId: int, name: str):
    return crud.update_track(trackId, name)


@app.delete("/authors/{authorId}", summary="Удаляет исполнителя из базы")
async def delete_author(authorId: int):
    return crud.delete_author(authorId)


@app.delete("/albums/{albumId}", summary="Удаляет альбом из базы")
async def delete_album(albumId: int):
    return crud.delete_album(albumId)


@app.delete("/tracks/{trackId}", summary="Удаляет трек из базы")
async def delete_track(trackId: int):
    return crud.delete_track(trackId)
