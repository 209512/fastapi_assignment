# app/models/reviews.py

from app.configs.database import get_client

async def create_review(user_id: int, movie_id: int, title: str, content: str, review_image_url: str | None):
    client = await get_client()
    query = """
        insert Review {
            user := (select User filter .id = <int64>$user_id),
            movie := (select Movie filter .id = <int64>$movie_id),
            title := <str>$title,
            content := <str>$content,
            review_image_url := <str?>$review_image_url
        }
    """
    return await client.query_single(query,
                                     user_id=user_id,
                                     movie_id=movie_id,
                                     title=title,
                                     content=content,
                                     review_image_url=review_image_url)

async def get_review_by_id(review_id: int):
    client = await get_client()
    query = """
        select Review {
            id,
            title,
            content,
            review_image_url,
            created_at,
            user: { id },
            movie: { id }
        }
        filter .id = <int64>$review_id
    """
    return await client.query_single(query, review_id=review_id)

async def update_review_by_id(review_id: int, title: str, content: str, review_image_url: str | None):
    client = await get_client()
    query = """
        update Review
        filter .id = <int64>$review_id
        set {
            title := <str>$title,
            content := <str>$content,
            review_image_url := <str?>$review_image_url
        }
    """
    return await client.query_single(query, review_id=review_id, title=title, content=content, review_image_url=review_image_url)

async def delete_review_by_id(review_id: int):
    client = await get_client()
    query = """
        delete Review
        filter .id = <int64>$review_id
    """
    result = await client.query(query, review_id=review_id)
    return bool(result)

async def list_reviews_by_user(user_id: int):
    client = await get_client()
    query = """
        select Review {
            id,
            title,
            content,
            review_image_url,
            created_at,
            user: { id },
            movie: { id }
        }
        filter .user.id = <int64>$user_id
        order by .created_at desc
    """
    return await client.query(query, user_id=user_id)

async def list_reviews_by_movie(movie_id: int):
    client = await get_client()
    query = """
        select Review {
            id,
            title,
            content,
            review_image_url,
            created_at,
            user: { id },
            movie: { id }
        }
        filter .movie.id = <int64>$movie_id
        order by .created_at desc
    """
    return await client.query(query, movie_id=movie_id)