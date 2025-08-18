# app/routers/movies.py

from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import Annotated

from app.models.movies import MovieModel
from app.schemas.movies import MovieCreate, MovieUpdate, MovieResponse

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("", response_model=list[MovieResponse])
def list_movies(
    title: Annotated[str | None, Query(min_length=1)] = None,
    genre: Annotated[str | None, Query(min_length=1)] = None,
):
    if title or genre:
        movies = MovieModel.filter(title=title if title else None, genre=genre if genre else None)
        if genre:
            movies = [m for m in movies if genre in m.genre]
    else:
        movies = MovieModel.all()
    return [MovieResponse(id=m.id, title=m.title, playtime=m.playtime, genre=m.genre) for m in movies]
