# app/routers/users.py

from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import datetime, timezone
from app.utils.file import validate_image_extension, upload_file, delete_file
from app.utils.jwt import create_access_token
from app.utils.auth import get_current_user
from app.schemas.users import (
    UserCreate, UserCreateResponse, UserResponse,
    FollowResponse, FollowingUserResponse, FollowerUserResponse
)
from app.models.users import (
    create_user, authenticate_user, get_all_users as users_all,
    update_last_login, update_user_profile_image_url,
    get_follow, create_follow, update_follow_is_following, get_followings, get_followers,
)

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

    if current_user.get("profile_image_url"):
        delete_file(current_user["profile_image_url"])

    url = await upload_file(file, "profiles")
    updated_user = await update_user_profile_image_url(current_user["id"], url)

    if not updated_user:
        raise HTTPException(status_code=500, detail="Failed to update profile image URL")

    return updated_user

@router.post("/{user_id}/follow", response_model=FollowResponse, status_code=200)
async def follow_user(user_id: int, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user["id"] == user_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")

    follow = await get_follow(follower_id=current_user["id"], following_id=user_id)
    if follow:
        if not follow.is_following:
            await update_follow_is_following(follow.id, True)
            follow.is_following = True
    else:
        follow = await create_follow(follower_id=current_user["id"], following_id=user_id, is_following=True)

    return FollowResponse(
        follower_id=follow.follower.id,
        following_id=follow.following.id,
        is_following=follow.is_following,
    )

@router.post("/{user_id}/unfollow", response_model=FollowResponse, status_code=200)
async def unfollow_user(user_id: int, current_user: Annotated[dict, Depends(get_current_user)]):
    if current_user["id"] == user_id:
        raise HTTPException(status_code=400, detail="Cannot unfollow yourself")

    follow = await get_follow(follower_id=current_user["id"], following_id=user_id)
    if follow:
        if follow.is_following:
            await update_follow_is_following(follow.id, False)
            follow.is_following = False
        return FollowResponse(
            follower_id=follow.follower.id,
            following_id=follow.following.id,
            is_following=follow.is_following,
        )
    else:
        return FollowResponse(
            follower_id=current_user["id"],
            following_id=user_id,
            is_following=False,
        )

@router.get("/followings", response_model=list[FollowingUserResponse], status_code=200)
async def get_followings_list(current_user: Annotated[dict, Depends(get_current_user)]):
    followings = await get_followings(user_id=current_user["id"])
    response = []
    for follow in followings:
        response.append(FollowingUserResponse(
            following_id=follow.following.id,
            username=follow.following.username,
            profile_image_url=follow.following.profile_image_url,
        ))
    return response

@router.get("/followers", response_model=list[FollowerUserResponse], status_code=200)
async def get_followers_list(current_user: Annotated[dict, Depends(get_current_user)]):
    followers = await get_followers(user_id=current_user["id"])
    response = []
    for follow in followers:
        response.append(FollowerUserResponse(
            follower_id=follow.follower.id,
            username=follow.follower.username,
            profile_image_url=follow.follower.profile_image_url,
        ))
    return response