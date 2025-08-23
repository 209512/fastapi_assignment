# app/schemas/likes.py

from enum import Enum
from pydantic import BaseModel

class ReactionTypeEnum(str, Enum):
    like = "like"
    dislike = "dislike"

class MovieReactionResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    type: ReactionTypeEnum

class MovieReactionCountResponse(BaseModel):
    movie_id: int
    like_count: int
    dislike_count: int

class ReviewLikeResponse(BaseModel):
    id: int
    user_id: int
    review_id: int
    is_liked: bool

class ReviewLikeCountResponse(BaseModel):
    review_id: int
    like_count: int

class ReviewIsLikedResponse(BaseModel):
    review_id: int
    user_id: int
    is_liked: bool