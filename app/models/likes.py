# app/models/likes.py

from app.configs.database import get_client

async def get_reviewlike(user_id: int, review_id: int):
    client = await get_client()
    query = """
        select ReviewLike
        filter .user.id = <int64>$user_id and .review.id = <int64>$review_id
    """
    return await client.query_single(query, user_id=user_id, review_id=review_id)

async def create_reviewlike(user_id: int, review_id: int, is_liked: bool = True):
    existing = await get_reviewlike(user_id, review_id)
    if existing:
        # 중복 생성 방지 - 필요하면 리턴 None 혹은 업데이트 로직 수행
        return None
    client = await get_client()
    query = """
        insert ReviewLike {
            user := (select User filter .id = <int64>$user_id),
            review := (select Review filter .id = <int64>$review_id),
            is_liked := <bool>$is_liked
        }
    """
    return await client.query_single(query, user_id=user_id, review_id=review_id, is_liked=is_liked)

async def update_reviewlike_is_liked(reviewlike_id: int, is_liked: bool):
    client = await get_client()
    query = """
        update ReviewLike
        filter .id = <int64>$reviewlike_id
        set { is_liked := <bool>$is_liked }
    """
    return await client.query_single(query, reviewlike_id=reviewlike_id, is_liked=is_liked)

async def count_likes_by_review(review_id: int) -> int:
    client = await get_client()
    query = """
        select count(ReviewLike)
        filter .review.id = <int64>$review_id and .is_liked = true
    """
    result = await client.query(query, review_id=review_id)
    return result[0] if result else 0

async def get_moviereaction(user_id: int, movie_id: int):
    client = await get_client()
    query = """
        select MovieLike
        filter .user.id = <int64>$user_id and .movie.id = <int64>$movie_id
    """
    return await client.query_single(query, user_id=user_id, movie_id=movie_id)

async def create_moviereaction(user_id: int, movie_id: int, type: str):
    client = await get_client()
    query = """
        insert MovieLike {
            user := (select User filter .id = <int64>$user_id),
            movie := (select Movie filter .id = <int64>$movie_id),
            type := <str>$type,
            created_at := <datetime>$now
        }
    """
    now = datetime.now(timezone.utc)
    return await client.query_single(query, user_id=user_id, movie_id=movie_id, type=type, now=now)

async def update_moviereaction_type(moviereaction_id: int, type: str):
    client = await get_client()
    query = """
        update MovieLike
        filter .id = <int64>$moviereaction_id
        set { type := <str>$type }
    """
    return await client.query_single(query, moviereaction_id=moviereaction_id, type=type)

async def count_reactions_by_movie(movie_id: int):
    client = await get_client()
    query_like = """
        select count(MovieLike)
        filter .movie.id = <int64>$movie_id and .type = "like"
    """
    query_dislike = """
        select count(MovieLike)
        filter .movie.id = <int64>$movie_id and .type = "dislike"
    """
    like_result = await client.query(query_like, movie_id=movie_id)
    dislike_result = await client.query(query_dislike, movie_id=movie_id)
    like_count = like_result[0] if like_result else 0
    dislike_count = dislike_result[0] if dislike_result else 0
    return like_count, dislike_count