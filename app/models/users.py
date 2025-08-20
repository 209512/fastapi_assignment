# app/models/users.py

from app.configs.database import get_client
from passlib.context import CryptContext

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