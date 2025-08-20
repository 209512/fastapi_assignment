# app/routers/users.py

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import datetime, timezone
from app.utils.jwt import create_access_token
from app.utils.auth import get_current_user
from app.models.users import create_user, authenticate_user, update_last_login, get_all_users as users_all
from app.schemas.users import UserCreate, UserCreateResponse, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

# 유저 생성 API
@router.post("/create", response_model=UserCreateResponse)
async def create_user_endpoint(user: UserCreate):
    new_user = await create_user(user.username, user.password, user.age, user.gender)
    return UserCreateResponse(id=new_user.id)

# 모든 유저 리스트 조회 API
@router.get("", response_model=list[UserResponse])
async def get_all_users():
    users = await users_all()
    return users

# 로그인 API (OAuth2PasswordRequestForm 이용)
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    await update_last_login(user.id)  # 로그인 시간 갱신
    # 로그인 시간 업데이트 로직 적용 시 필요
    token = create_access_token(data={"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

# 현재 로그인 유저 정보 조회 API
@router.get("/me", response_model=UserResponse)
async def get_me(current_user: Annotated[dict, Depends(get_current_user)]):
    return current_user