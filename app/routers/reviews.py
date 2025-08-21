# app/routers/reviews.py

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Path, status
from typing import Annotated
from app.utils.auth import get_current_user
from app.utils.file import validate_image_extension, upload_file, delete_file
from app.models.reviews import create_review, get_review_by_id, update_review_by_id, delete_review_by_id, list_reviews_by_user, list_reviews_by_movie
from app.schemas.reviews import ReviewResponse

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review_endpoint(
    movie_id: int = Form(...),
    title: str = Form(..., max_length=50),
    content: str = Form(..., max_length=255),
    review_image: UploadFile | None = File(None),
    current_user=Depends(get_current_user)
):
    image_url: str | None = None
    if review_image:
        validate_image_extension(review_image)
        image_url = await upload_file(review_image, "reviews")

    review = await create_review(
        user_id=current_user.id,
        movie_id=movie_id,
        title=title,
        content=content,
        review_image_url=image_url
    )

    if not review:
        raise HTTPException(status_code=500, detail="Failed to create review")

    return review

@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(review_id: int = Path(..., gt=0)):
    review = await get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.put("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: int = Path(..., gt=0),
    title: str = Form(..., max_length=50),
    content: str = Form(..., max_length=255),
    review_image: UploadFile | None = File(None),
    current_user=Depends(get_current_user)
):
    review = await get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this review")

    image_url = review.review_image_url
    if review_image:
        validate_image_extension(review_image)
        # 기존 이미지 삭제
        if image_url:
            delete_file(image_url)
        image_url = await upload_file(review_image, "reviews")

    updated = await update_review_by_id(review_id, title, content, image_url)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update review")

    return updated

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: int = Path(..., gt=0),
    current_user=Depends(get_current_user)
):
    review = await get_review_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this review")

    deleted = await delete_review_by_id(review_id)
    if not deleted:
        raise HTTPException(status_code=500, detail="Failed to delete review")
    return

@router.get("/users/me/reviews", response_model=list[ReviewResponse])
async def get_my_reviews(current_user=Depends(get_current_user)):
    reviews = await list_reviews_by_user(current_user.id)
    return reviews

@router.get("/movies/{movie_id}/reviews", response_model=list[ReviewResponse])
async def get_movie_reviews(movie_id: int = Path(..., gt=0)):
    reviews = await list_reviews_by_movie(movie_id)
    return reviews