# main.py

from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, Query, status
from app.models.users import UserModel
from app.schemas.users import UserCreate, UserCreateResponse, UserResponse, UserUpdate, UserSearchQuery, GenderEnum
from app.models.movies import MovieModel
from app.schemas.movies import MovieCreate, MovieUpdate, MovieResponse

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
    return UserCreateResponse(id=new_user.id)

@app.get("/users", response_model=list[UserResponse])
def get_all_users():
    users = UserModel.all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: Annotated[int, Path(..., gt=0, description="User ID must be positive")]
):
    user = UserModel.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.patch("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: Annotated[int, Path(..., gt=0)],
    user_update: UserUpdate = ...
):
    user = UserModel.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.update(username=user_update.username, age=user_update.age)
    return user

@app.delete("/users/{user_id}")
def delete_user(
        user_id: Annotated[int, Path(..., gt=0)]
):
    user = UserModel.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete()
    return {"detail": f"User: {user_id}, Successfully Deleted."}

@app.get("/users/search", response_model=list[UserResponse])
def search_users(
    username: Annotated[str | None, Query(min_length=1, max_length=50)] = None,
    age: Annotated[int | None, Query(gt=0)] = None,
    gender: GenderEnum | None = None
):
    query_data = UserSearchQuery(username=username, age=age, gender=gender)

    filters = {}
    if query_data.username:
        filters["username"] = query_data.username
    if query_data.age:
        filters["age"] = query_data.age
    if query_data.gender:
        filters["gender"] = query_data.gender

    users = UserModel.filter(**filters)
    if not users:
        raise HTTPException(status_code=404, detail="No matching users found")
    return users

# 1. 영화 등록 API
@app.post("/movie/create", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate):
    instance = MovieModel.create(movie.title, movie.playtime, movie.genre)
    return MovieResponse(id=instance.id, title=instance.title, playtime=instance.playtime, genre=instance.genre)

# 2. 전체 영화 검색 및 리스트 조회 API
@app.get("/movies", response_model=list[MovieResponse])
def list_movies(
    title: Annotated[str | None, Query(min_length=1)] = None,
    genre: Annotated[str | None, Query(min_length=1)] = None,
):
    if title or genre:
        movies = MovieModel.filter(
            title=title if title else None,
            genre=genre if genre else None,
        )
        if genre:
            movies = [m for m in movies if genre in m.genre]
    else:
        movies = MovieModel.all()
    return [MovieResponse(id=m.id, title=m.title, playtime=m.playtime, genre=m.genre) for m in movies]

# 3. 특정 영화 상세 조회 API
@app.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: Annotated[int, Path(..., gt=0)]):
    movie = MovieModel.get(id=movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return MovieResponse(id=movie.id, title=movie.title, playtime=movie.playtime, genre=movie.genre)

# 4. 특정 영화 정보 수정 API
@app.patch("/movies/{movie_id}", response_model=MovieResponse)
def update_movie(
        movie_id: Annotated[int, Path(..., gt=0, description="Movie ID must be a positive integer")],
        movie_update: MovieUpdate = ...,
):
    movie = MovieModel.get(id=movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = movie_update.model_dump(exclude_unset=True)
    movie.update(**update_data)

    return MovieResponse(id=movie.id, title=movie.title, playtime=movie.playtime, genre=movie.genre)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)