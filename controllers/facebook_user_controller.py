# facebook_user_controller.py
from fastapi import APIRouter, HTTPException
from models.facebook_user import FacebookUser
from typing import List

router = APIRouter()

@router.post("/", response_model=FacebookUser)
async def create_facebook_user(facebook_user: FacebookUser):
    return await facebook_user.create()

@router.get("/", response_model=List[FacebookUser])
async def read_facebook_users():
    return await FacebookUser.read_all()

@router.get("/{facebook_user_id}", response_model=FacebookUser)
async def read_facebook_user(facebook_user_id: int):
    facebook_user = await FacebookUser.read(facebook_user_id)
    if facebook_user is None:
        raise HTTPException(status_code=404, detail="Facebook User not found")
    return facebook_user

@router.put("/{facebook_user_id}", response_model=FacebookUser)
async def update_facebook_user(facebook_user_id: int, facebook_user: FacebookUser):
    return await facebook_user.update(facebook_user_id)

@router.delete("/{facebook_user_id}")
async def delete_facebook_user(facebook_user_id: int):
    return await facebook_user.delete(facebook_user_id)
