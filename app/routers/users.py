# app/routers/users.py

from fastapi import APIRouter, HTTPException, Path, Query
from typing import Annotated

from app.models.users import UserModel
from app.schemas.users import (
    UserCreate, UserCreateResponse, UserResponse,
    UserUpdate, UserSearchQuery, GenderEnum
)

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/create", response_model=UserCreateResponse)
def create_user(user: UserCreate):
    new_user = UserModel.create(
        username=user.username,
        password="changeme",   # 일단 임시
        age=user.age,
        gender=user.gender,
    )
    return UserCreateResponse(id=new_user.id)

@router.get("", response_model=list[UserResponse])
def get_all_users():
    users = UserModel.all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users
