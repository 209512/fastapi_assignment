# app/routers/users.py

from fastapi import APIRouter, HTTPException, Path, Query, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import datetime, timezone
from app.utils.jwt import create_access_token, get_current_user
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
        password=user.password,
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

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = UserModel.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    user.last_login = datetime.now(timezone.utc)
    token = create_access_token(data={"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: Annotated[UserModel, Depends(get_current_user)]):
    return current_user