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

async def list_movies(title: str | None = None, genre: str | None = None):
    client = await get_client()
    base_query = "select Movie { id, title, playtime, genre, cast }"
    conditions = []
    params = {}

    if title:
        conditions.append("contains(.title, <str>$title)")
        params["title"] = title
    if genre:
        conditions.append(".genre = <str>$genre")
        params["genre"] = genre

    if conditions:
        where_clause = " filter " + " and ".join(conditions)
    else:
        where_clause = ""

    query = base_query + where_clause + " order by .created_at desc"
    return await client.query(query, **params)

async def get_movie_by_id(movie_id: int):
    client = await get_client()
    query = """
        select Movie {
            id,
            title,
            playtime,
            genre,
            cast
        }
        filter .id = <int64>$movie_id
    """
    return await client.query_single(query, movie_id=movie_id)

async def update_movie_by_id(movie_id: int, movie_update):
    client = await get_client()
    query = """
        update Movie
        filter .id = <int64>$movie_id
        set {
            title := <str>$title,
            playtime := <int16>$playtime,
            genre := <str>$genre,
            cast := <json>$cast
        }
    """
    updated = await client.query_single(
        query,
        movie_id=movie_id,
        title=movie_update.title,
        playtime=movie_update.playtime,
        genre=movie_update.genre,
        cast=movie_update.cast,
    )
    return updated

async def delete_movie_by_id(movie_id: int):
    client = await get_client()
    query = """
        delete Movie
        filter .id=<int64>$movie_id
    """
    result = await client.query(query, movie_id=movie_id)
    # GelDB delete 쿼리는 리스트 반환, 삭제된 항목이 있으면 True
    return bool(result)