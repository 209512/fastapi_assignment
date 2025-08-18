# main.py

from fastapi import FastAPI
from app.models.users import UserModel
from app.models.movies import MovieModel
from app.routers import users, movies

app = FastAPI()

UserModel.create_dummy()
MovieModel.create_dummy()

app.include_router(users.router, tags=["users"])
app.include_router(movies.router, tags=["movies"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)