# app/schemas/movies.py

from pydantic import BaseModel, Field

class MovieCreate(BaseModel):
    title: str = Field(..., min_length=1)
    playtime: int = Field(..., gt=0)
    genre: list[str] = Field(..., min_items=1)

class MovieResponse(BaseModel):
    id: int
    title: str
    playtime: int
    genre: list[str]

class MovieSearchQuery(BaseModel):
    title: str | None = Field(None, min_length=1)
    genre: str | None = Field(None, min_length=1)