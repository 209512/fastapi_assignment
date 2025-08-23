# app/schemas/users.py

from enum import Enum
from pydantic import BaseModel, Field

class GenderEnum(str, Enum):
    male = "male"
    female = "female"

class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50) # ...은 필수 필드 표시. 해당 필드 누락 시 유효성 검사 단계에서 422 Unprocessable Entity 오류 발생
    age: int = Field(..., gt=0, le=120)
    gender: GenderEnum

class UserCreateResponse(BaseModel):
    id: int

class UserResponse(BaseModel):
    id: int
    username: str
    age: int
    gender: GenderEnum
    profile_image_url: str | None = None

class UserUpdate(BaseModel):
    username: str | None = Field(None, min_length=1, max_length=50)
    age: int | None = Field(None, gt=0, le=120)

class UserSearchQuery(BaseModel):
    username: str | None = Field(None, min_length=1, max_length=50)
    age: int | None = Field(None, gt=0)
    gender: GenderEnum | None = None

class FollowResponse(BaseModel):
    follower_id: int
    following_id: int
    is_following: bool

class FollowingUserResponse(BaseModel):
    following_id: int
    username: str
    profile_image_url: str | None = None

class FollowerUserResponse(BaseModel):
    follower_id: int
    username: str
    profile_image_url: str | None = None