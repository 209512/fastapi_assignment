# app/models/users.py

from app.configs.database import get_client
from passlib.context import CryptContext
from datetime import datetime, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def create_user(username: str, password: str, age: int, gender: str):
    client = await get_client()
    hashed_password = await hash_password(password)
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
    verified = pwd_context.verify(password, user.hashed_password)
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