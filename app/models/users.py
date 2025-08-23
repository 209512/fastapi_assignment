# app/models/users.py

from app.configs.database import get_client
from passlib.context import CryptContext
from datetime import datetime, timezone
import asyncio

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

async def create_user(username: str, password: str, age: int, gender: str):
    client = await get_client()
    hashed_password = hash_password(password)
    query = """
        insert User {
            username := <str>$username,
            hashed_password := <str>$hashed_password,
            age := <int16>$age,
            gender := <str>$gender
        }
    """
    return await client.query_single(
        query,
        username=username,
        hashed_password=hashed_password,
        age=age,
        gender=gender,
    )

async def authenticate_user(username: str, password: str):
    client = await get_client()
    query = """
        select User {
            id,
            username,
            hashed_password,
            age,
            gender,
            last_login
        }
        filter .username = <str>$username
    """
    user = await client.query_single(query, username=username)
    if not user:
        return None

    verified = verify_password(password, user.hashed_password)
    if not verified:
        return None
    return user

async def get_all_users():
    client = await get_client()
    query = """
        select User {
            id,
            username,
            age,
            gender
        }
        order by .created_at desc
    """
    users = await client.query(query)
    return users

async def update_last_login(user_id: int):
    client = await get_client()
    now = datetime.now(timezone.utc)
    query = """
        update User
        filter .id = <int64>$user_id
        set {
            last_login := <datetime>$now
        }
    """
    await client.query(query, user_id=user_id, now=now)

async def update_user_profile_image_url(user_id: int, url: str | None):
    client = await get_client()
    query = """
        update User
        filter .id = <int64>$user_id
        set {
            profile_image_url := <str?>$url
        }
    """
    updated = await client.query_single(query, user_id=user_id, url=url)
    return updated

async def get_follow(follower_id: int, following_id: int):
    client = await get_client()
    query = """
        select Follow
        filter .follower.id = <int64>$follower_id and .following.id = <int64>$following_id
    """
    return await client.query_single(query, follower_id=follower_id, following_id=following_id)

async def create_follow(follower_id: int, following_id: int, is_following: bool = True):
    client = await get_client()
    query = """
        insert Follow {
            follower := (select User filter .id = <int64>$follower_id),
            following := (select User filter .id = <int64>$following_id),
            is_following := <bool>$is_following,
            created_at := <datetime>$now
        }
    """
    now = datetime.now(timezone.utc)
    return await client.query_single(query, follower_id=follower_id, following_id=following_id, is_following=is_following, now=now)

async def update_follow_is_following(follow_id: int, is_following: bool):
    client = await get_client()
    query = """
        update Follow
        filter .id = <int64>$follow_id
        set {
            is_following := <bool>$is_following
        }
    """
    return await client.query_single(query, follow_id=follow_id, is_following=is_following)

async def get_followings(user_id: int):
    client = await get_client()
    query = """
        select Follow {
            following: {
                id,
                username,
                profile_image_url
            }
        }
        filter .follower.id = <int64>$user_id and .is_following = true
    """
    return await client.query(query, user_id=user_id)

async def get_followers(user_id: int):
    client = await get_client()
    query = """
        select Follow {
            follower: {
                id,
                username,
                profile_image_url
            }
        }
        filter .following.id = <int64>$user_id and .is_following = true
    """
    return await client.query(query, user_id=user_id)