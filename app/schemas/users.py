# app/schemas/users.py

from enum import Enum
from pydantic import BaseModel, Field

# gender field: enum
class GenderEnum(str, Enum):
    male = "male"
    female = "female"

# Request Body 검증 모델
class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    age: int = Field(gt=0, le=120)
    gender: GenderEnum

# 유저 생성 응답 모델
class UserCreateResponse(BaseModel):
    id: int

# 모든 유저 정보 반환 모델
class UserResponse(BaseModel):
    id: int
    username: str
    age: int
    gender: GenderEnum