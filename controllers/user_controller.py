# user_controller.py
from fastapi import APIRouter, HTTPException
from models.user import User
from typing import List

router = APIRouter()

@router.post("/", response_model=User)
async def create_user(user: User):
    return await user.create()

@router.get("/", response_model=List[User])
async def read_users():
    return await User.read_all()

@router.get("/{user_id}", response_model=User)
async def read_user(user_id: int):
    user = await User.read(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    return await user.update(user_id)

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    return await user.delete(user_id)
