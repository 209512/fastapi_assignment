# app/utils/file.py

import os
import uuid
from typing import Union
from fastapi import UploadFile, File, HTTPException
from app.configs.base import settings

IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "gif"]

async def upload_file(file: Union[File, UploadFile], upload_dir: str) -> str:
    filename, ext = os.path.splitext(file.filename if isinstance(file, UploadFile) else file.name)
    ext = ext.lstrip(".").lower()

    unique_filename = f"{filename}_{uuid.uuid4().hex}.{ext}"
    save_dir = settings.MEDIA_DIR / upload_dir
    save_dir.mkdir(parents=True, exist_ok=True)

    file_path = save_dir / unique_filename

    if isinstance(file, UploadFile):
        # async read & write
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    else:
        # file is a direct File bytes-like
        with open(file_path, "wb") as buffer:
            buffer.write(file)

    return f"/{upload_dir}/{unique_filename}"

def delete_file(file_url: str) -> None:
    file_path = settings.MEDIA_DIR / file_url.lstrip("/")
    if file_path.exists():
        file_path.unlink()

def validate_image_extension(file: Union[File, UploadFile]) -> str:
    filename = file.filename if isinstance(file, UploadFile) else getattr(file, "name", "")
    ext = filename.split(".")[-1].lower()
    if ext not in IMAGE_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid image file extension")
    return ext
