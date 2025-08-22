# app/models/users.py

from app.configs.database import get_client
from passlib.context import CryptContext
from datetime import datetime, timezone
import asyncio

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- 수정된 코드 ---

# 동기 함수로 정의
# hash()는 CPU 집약적인 동기 작업이므로, async def가 아닌 def로 정의하는 것이 올바름
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 동기 함수로 정의
def verify_password(password: str, hashed_password: str) -> bool:
    """주어진 비밀번호와 해싱된 비밀번호를 비교"""
    return pwd_context.verify(password, hashed_password)

# -----------------

async def create_user(username: str, password: str, age: int, gender: str):
    client = await get_client()
    # async def 안에서 동기 함수를 호출할 때 await를 붙이지 x
    # FastAPI는 이 동기 함수를 스레드 풀에서 실행해 이벤트 루프를 블로킹하지 않도록 자동 처리
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

    # 비동기 함수 안에서 동기 함수 호출 시 await를 붙이지 않으며,
    # FastAPI가 내부적으로 스레드 풀을 이용해 안전하게 처리
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