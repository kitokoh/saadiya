# group_user_controller.py
from fastapi import APIRouter, HTTPException
from models.group_user import GroupUser
from typing import List

router = APIRouter()

@router.post("/", response_model=GroupUser)
async def create_group_user(group_user: GroupUser):
    return await group_user.create()

@router.get("/", response_model=List[GroupUser])
async def read_group_users():
    return await GroupUser.read_all()

@router.get("/{group_user_id}", response_model=GroupUser)
async def read_group_user(group_user_id: int):
    group_user = await GroupUser.read(group_user_id)
    if group_user is None:
        raise HTTPException(status_code=404, detail="Group User not found")
    return group_user

@router.put("/{group_user_id}", response_model=GroupUser)
async def update_group_user(group_user_id: int, group_user: GroupUser):
    return await group_user.update(group_user_id)

@router.delete("/{group_user_id}")
async def delete_group_user(group_user_id: int):
    return await group_user.delete(group_user_id)
