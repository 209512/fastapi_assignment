# main.py

from typing import List
from fastapi import FastAPI, HTTPException, Path
from app.models.users import UserModel
from app.schemas.users import UserCreate, UserCreateResponse, UserResponse, UserUpdate

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


# 3. 유저 상세 조회 API
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int = Path(..., gt=0, description="User ID must be positive")
):
    """
    경로 매개변수로 전달된 user_id 사용해
    해당 ID의 유저 조회.
    없으면 404 에러 반환.
    """
    user = UserModel.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# 4. 유저 일부 수정 API
@app.patch("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int = Path(..., gt=0),
    user_update: UserUpdate = ...
):
    """
    user_id로 유저 찾고,
    요청 바디(UserUpdate)의 값으로 username, age 부분 수정.
    존재하지 않으면 404 반환.
    """
    user = UserModel.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # None이 아닌 값만 업데이트
    user.update(username=user_update.username, age=user_update.age)
    return user


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)