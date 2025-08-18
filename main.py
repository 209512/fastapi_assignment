# main.py

from typing import List, Optional # Annotated 사용시 한번 타입 선언으로 타입힌트, 추가정보 함께 명시 가능 /복잡한 타입 명시에 사용
from fastapi import FastAPI, HTTPException, Path, Query, status
from app.models.users import UserModel
from app.schemas.users import UserCreate, UserCreateResponse, UserResponse, UserUpdate, UserSearchQuery
from app.models.movies import MovieModel
from app.schemas.movies import MovieCreate, MovieResponse

app = FastAPI()

UserModel.create_dummy() # API 테스트를 위한 더미를 생성하는 메서드 입니다.
MovieModel.create_dummy()

@app.post("/user/create", response_model=UserCreateResponse)
def create_user(user: UserCreate):
    new_user = UserModel.create(
        username=user.username,
        age=user.age,
        gender=user.gender,
    )
    return {'id': new_user.id}

@app.get("/users", response_model=List[UserResponse])
def get_all_users():
    users = UserModel.all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int = Path(..., gt=0, description="User ID must be positive")
):
    user = UserModel.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.patch("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int = Path(..., gt=0),
    user_update: UserUpdate = ...
):
    user = UserModel.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.update(username=user_update.username, age=user_update.age)
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int = Path(..., gt=0)):
    user = UserModel.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete()
    return {"detail": f"User: {user_id}, Successfully Deleted."}

@app.get("/users/search", response_model=List[UserResponse])
def search_users(
    username: Optional[str] = Query(None, min_length=1, max_length=50),
    age: Optional[int] = Query(None, gt=0),
    gender: Optional[str] = Query(None)
):
    try:
        query_data = UserSearchQuery(
            username=username,
            age=age,
            gender=gender
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    filters = {}
    if query_data.username: filters["username"] = query_data.username
    if query_data.age: filters["age"] = query_data.age
    if query_data.gender: filters["gender"] = query_data.gender

    users = UserModel.filter(**filters)
    if not users:
        raise HTTPException(status_code=404, detail="No matching users found")
    return users

# 1. 영화 등록 API
@app.post("/movie/create", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate):
    instance = MovieModel.create(movie.title, movie.playtime, movie.genre)
    return MovieResponse(id=instance.id, title=instance.title, playtime=instance.playtime, genre=instance.genre)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)