# media_controller.py
from fastapi import APIRouter, HTTPException
from models.media import Media
from typing import List

router = APIRouter()

@router.post("/", response_model=Media)
async def create_media(media: Media):
    return await media.create()

@router.get("/", response_model=List[Media])
async def read_media():
    return await Media.read_all()

@router.get("/{media_id}", response_model=Media)
async def read_media_item(media_id: int):
    media = await Media.read(media_id)
    if media is None:
        raise HTTPException(status_code=404, detail="Media not found")
    return media

@router.put("/{media_id}", response_model=Media)
async def update_media(media_id: int, media: Media):
    return await media.update(media_id)

@router.delete("/{media_id}")
async def delete_media(media_id: int):
    return await media.delete(media_id)
