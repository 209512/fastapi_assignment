from typing import List
from pydantic import BaseModel, Field

class MovieCreate(BaseModel):
    title: str = Field(..., min_length=1)
    playtime: int = Field(..., gt=0)
    genre: List[str] = Field(..., min_items=1)

class MovieResponse(BaseModel):
    id: int
    title: str
    playtime: int
    genre: List[str]
