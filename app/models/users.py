# app/models/users.py

from app.configs.database import get_client
from passlib.context import CryptContext
from datetime import datetime, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 비밀번호 해싱 함수
async def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 유저 생성 함수 (insert User)
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

# 유저 인증 함수 (select후 비밀번호 검증)
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

# 모든 유저 조회 함수
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

# 로그인 시간 업데이트 함수
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