# app/routers/movies.py

from fastapi import APIRouter, HTTPException, Query, Path, UploadFile, File, HTTPException
from typing import Annotated
from app.utils.file import validate_image_extension, upload_file, delete_file
from app.schemas.movies import MovieCreate, MovieResponse, MovieUpdate
from app.models.movies import create_movie, get_movie_by_id, list_movies, update_movie_by_id, delete_movie_by_id, update_movie_poster_image_url

router = APIRouter(prefix="/movies", tags=["movies"])

@router.post("", response_model=MovieResponse)
async def add_movie(movie: MovieCreate):
    new_movie = await create_movie(
        title=movie.title,
        playtime=movie.playtime,
        genre=movie.genre,
        cast=movie.cast
    )
    return new_movie

@router.get("", response_model=list[MovieResponse])
async def list_movies_endpoint(
    title: Annotated[str | None, Query(min_length=1)] = None,
    genre: Annotated[str | None, Query(min_length=1)] = None
):
    movies = await list_movies(title=title, genre=genre)
    return movies

@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie(movie_id: Annotated[int, Path(gt=0)]):
    movie = await get_movie_by_id(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.put("/{movie_id}", response_model=MovieResponse)
async def update_movie(movie_id: Annotated[int, Path(gt=0)], movie_update: MovieUpdate):
    updated = await update_movie_by_id(movie_id, movie_update)
    if updated is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated

@router.delete("/{movie_id}")
async def delete_movie(movie_id: Annotated[int, Path(gt=0)]):
    deleted = await delete_movie_by_id(movie_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"detail": "Movie deleted successfully"}

@router.post("/{movie_id}/poster_image", response_model=MovieResponse)
async def upload_poster_image(
    movie_id: int = Path(..., gt=0),
    file: UploadFile = File(...)
):
    movie = await get_movie_by_id(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    validate_image_extension(file)

    if movie.poster_image_url:
        delete_file(movie.poster_image_url)

    url = await upload_file(file, "posters")
    updated_movie = await update_movie_poster_image_url(movie_id, url)

    if not updated_movie:
        raise HTTPException(status_code=500, detail="Failed to update poster image URL")

    return updated_movie