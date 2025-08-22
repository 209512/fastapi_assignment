# app/routers/likes.py

from fastapi import APIRouter, Depends, HTTPException, Path, status
from app.utils.auth import get_current_user
from app.models.likes import (
    get_reviewlike, create_reviewlike, update_reviewlike_is_liked, count_likes_by_review,
    get_moviereaction, create_moviereaction, update_moviereaction_type, count_reactions_by_movie,
)
from app.schemas.likes import (
    ReviewLikeResponse, ReviewLikeCountResponse, ReviewIsLikedResponse,
    MovieReactionResponse, MovieReactionCountResponse, ReactionTypeEnum,
)


router = APIRouter(prefix="/likes", tags=["likes"])

@router.post("/reviews/{review_id}/like", response_model=ReviewLikeResponse)
async def like_review(review_id: int = Path(..., gt=0), current_user=Depends(get_current_user)):
    existing_like = await get_reviewlike(current_user.id, review_id)
    if existing_like:
        if not existing_like.is_liked:
            updated = await update_reviewlike_is_liked(existing_like.id, True)
            return updated
        return existing_like
    new_like = await create_reviewlike(current_user.id, review_id)
    return new_like

@router.post("/reviews/{review_id}/unlike", response_model=ReviewLikeResponse)
async def unlike_review(review_id: int = Path(..., gt=0), current_user=Depends(get_current_user)):
    existing_like = await get_reviewlike(current_user.id, review_id)
    if not existing_like:
        # id None으로 반환
        return ReviewLikeResponse(id=None, user_id=current_user.id, review_id=review_id, is_liked=False)
    if existing_like.is_liked:
        updated = await update_reviewlike_is_liked(existing_like.id, False)
        return updated
    return existing_like

@router.get("/reviews/{review_id}/like_count", response_model=ReviewLikeCountResponse)
async def get_like_count(review_id: int = Path(..., gt=0)):
    count = await count_likes_by_review(review_id)
    return ReviewLikeCountResponse(review_id=review_id, like_count=count)

@router.get("/reviews/{review_id}/is_liked", response_model=ReviewIsLikedResponse)
async def is_liked_review(review_id: int = Path(..., gt=0), current_user=Depends(get_current_user)):
    review_like = await get_reviewlike(current_user.id, review_id)
    if not review_like:
        return ReviewIsLikedResponse(review_id=review_id, user_id=current_user.id, is_liked=False)
    return ReviewIsLikedResponse(review_id=review_id, user_id=current_user.id, is_liked=review_like.is_liked)

@router.post("/movies/{movie_id}/like", response_model=MovieReactionResponse, status_code=status.HTTP_200_OK)
async def like_movie(movie_id: int = Path(..., gt=0), current_user=Depends(get_current_user)):
    reaction = await get_moviereaction(current_user["id"], movie_id)
    if reaction:
        if reaction.type == ReactionTypeEnum.dislike:
            reaction = await update_moviereaction_type(reaction.id, ReactionTypeEnum.like)
    else:
        reaction = await create_moviereaction(current_user["id"], movie_id, ReactionTypeEnum.like)
    return reaction

@router.post("/movies/{movie_id}/dislike", response_model=MovieReactionResponse, status_code=status.HTTP_200_OK)
async def dislike_movie(movie_id: int = Path(..., gt=0), current_user=Depends(get_current_user)):
    reaction = await get_moviereaction(current_user["id"], movie_id)
    if reaction:
        if reaction.type == ReactionTypeEnum.like:
            reaction = await update_moviereaction_type(reaction.id, ReactionTypeEnum.dislike)
    else:
        reaction = await create_moviereaction(current_user["id"], movie_id, ReactionTypeEnum.dislike)
    return reaction

@router.get("/movies/{movie_id}/reaction_count", response_model=MovieReactionCountResponse, status_code=status.HTTP_200_OK)
async def get_movie_reaction_counts(movie_id: int = Path(..., gt=0)):
    like_count, dislike_count = await count_reactions_by_movie(movie_id)
    return MovieReactionCountResponse(
        movie_id=movie_id,
        like_count=like_count,
        dislike_count=dislike_count,
    )