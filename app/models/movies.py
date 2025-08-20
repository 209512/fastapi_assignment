# app/models/movies.py

from app.configs.database import get_client

# 영화 생성 함수
async def create_movie(title: str, plot: str, playtime: int, genre: str, cast: list):
    client = await get_client()
    query = """
        insert Movie {
            title := <str>$title,
            plot := <str>$plot,
            playtime := <int16>$playtime,
            genre := <str>$genre,
            cast := <json>$cast
        }
    """
    return await client.query_single(
        query,
        title=title,
        plot=plot,
        playtime=playtime,
        genre=genre,
        cast=cast,
    )