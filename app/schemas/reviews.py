# app/schemas/reviews.py

from pydantic import BaseModel
from datetime import datetime

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    title: str
    content: str
    review_image_url: str | None = None
    created_at: datetime