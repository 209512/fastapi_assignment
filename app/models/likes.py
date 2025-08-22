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