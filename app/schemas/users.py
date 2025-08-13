# app/schemas/users.py

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

# gender 값 제한 enum
class GenderEnum(str, Enum):
    male = "male"
    female = "female"

# Request Body 검증 모델
class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50) # ...은 필수 필드 표시. 해당 필드 누락 시 유효성 검사 단계에서 422 Unprocessable Entity 오류 발생
    age: int = Field(..., gt=0, le=120)
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

# Request Body에서 username, age 둘 중 일부만 수정해도 가능
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=50)
    age: Optional[int] = Field(None, gt=0, le=120)

# 쿼리 파라미터 검증 모델
class UserSearchQuery(BaseModel):
    username: Optional[str] = Field(None, min_length=1, max_length=50)
    age: Optional[int] = Field(None, gt=0)
    gender: Optional[GenderEnum]