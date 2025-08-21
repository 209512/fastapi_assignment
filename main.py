# main.py

from fastapi import FastAPI
from app.routers import users, movies, reviews, likes

app = FastAPI()

app.include_router(users.router)
app.include_router(movies.router)
app.include_router(reviews.router)
app.include_router(likes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)