# app/utils/auth.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.configs.base import settings
from app.models.users import authenticate_user, get_client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# 현재 로그인 유저 정보 조회
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    client = await get_client()
    query = """
        select User {
            id,
            username,
            age,
            gender,
            last_login
        }
        filter .id = <uuid>$user_id
    """
    user = await client.query_single(query, user_id=user_id)
    if user is None:
        raise credentials_exception
    return user