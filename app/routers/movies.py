# app/routers/movies.py

from fastapi import APIRouter, HTTPException, Query, Path
from typing import Annotated
from app.schemas.movies import MovieCreate, MovieResponse, MovieUpdate
from app.models.movies import create_movie, get_movie_by_id, list_movies, update_movie_by_id, delete_movie_by_id

router = APIRouter(prefix="/movies", tags=["movies"])

# 영화 등록 API
@router.post("", response_model=MovieResponse)
async def add_movie(movie: MovieCreate):
    new_movie = await create_movie(
        title=movie.title,
        playtime=movie.playtime,
        genre=movie.genre,
        cast=movie.cast
    )
    return new_movie

# 영화 조회 API (필터링 가능)
@router.get("", response_model=list[MovieResponse])
async def list_movies_endpoint(
    title: Annotated[str | None, Query(min_length=1)] = None,
    genre: Annotated[str | None, Query(min_length=1)] = None
):
    movies = await list_movies(title=title, genre=genre)
    return movies

# 영화 단일 조회 API
@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie(movie_id: Annotated[int, Path(gt=0)]):
    movie = await get_movie_by_id(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

# 영화 수정 API
@router.put("/{movie_id}", response_model=MovieResponse)
async def update_movie(movie_id: Annotated[int, Path(gt=0)], movie_update: MovieUpdate):
    updated = await update_movie_by_id(movie_id, movie_update)
    if updated is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated

# 영화 삭제 API
@router.delete("/{movie_id}")
async def delete_movie(movie_id: Annotated[int, Path(gt=0)]):
    deleted = await delete_movie_by_id(movie_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"detail": "Movie deleted successfully"}
