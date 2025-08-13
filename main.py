# main.py

from typing import List
from fastapi import FastAPI, HTTPException
from app.models.users import UserModel
from app.schemas.users import UserCreate, UserCreateResponse, UserResponse

app = FastAPI()

UserModel.create_dummy() # API 테스트를 위한 더미를 생성하는 메서드 입니다.

# 1. 유저 생성 API
@app.post("/user/create", response_model=UserCreateResponse)
def create_user(user: UserCreate):
    '''
    클라이언트 - username, age, gender 받아
    pydantic(usercreate)로 유효성 검증 후 usermodel에 저장,
    생성된 유저 Id 반환
    '''
    new_user = UserModel.create(
        username=user.username,
        age=user.age,
        gender=user.gender,
    )
    return {'id': new_user.id}


# 2. 모든 유저 조회 API
@app.get("/users", response_model=List[UserResponse])
def get_all_users():
    """
    모든 유저 데이터를 리스트로 반환.
    유저 없으면 404 에러 반환.
    """
    users = UserModel.all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)