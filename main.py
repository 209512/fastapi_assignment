# main.py

from typing import Annotated
from fastapi import FastAPI
from app.models.users import UserModel
from app.schemas.users import UserCreate, UserCreateResponse

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

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)