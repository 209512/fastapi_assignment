# app/routers/users.py

from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import datetime, timezone
from app.utils.file import validate_image_extension, upload_file, delete_file
from app.utils.jwt import create_access_token
from app.utils.auth import get_current_user
from app.models.users import create_user, authenticate_user, update_last_login, update_user_profile_image_url, get_all_users as users_all
from app.schemas.users import UserCreate, UserCreateResponse, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/create", response_model=UserCreateResponse)
async def create_user_endpoint(user: UserCreate):
    new_user = await create_user(user.username, user.password, user.age, user.gender)
    return UserCreateResponse(id=new_user.id)

@router.get("", response_model=list[UserResponse])
async def get_all_users():
    users = await users_all()
    return users

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    await update_last_login(user.id)
    token = create_access_token(data={"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: Annotated[dict, Depends(get_current_user)]):
    return current_user

@router.post("/me/profile_image", response_model=UserResponse)
async def upload_profile_image(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):
    validate_image_extension(file)

    # 기존 이미지 있으면 삭제
    if current_user.get("profile_image_url"):
        delete_file(current_user["profile_image_url"])

    # 업로드
    url = await upload_file(file, "profiles")
    updated_user = await update_user_profile_image_url(current_user["id"], url)

    # 업데이트 실패 예외 처리
    if not updated_user:
        raise HTTPException(status_code=500, detail="Failed to update profile image URL")

    return updated_user