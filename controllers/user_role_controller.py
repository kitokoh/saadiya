# user_role_controller.py
from fastapi import APIRouter, HTTPException
from models.user_role import UserRole
from typing import List

router = APIRouter()

@router.post("/", response_model=UserRole)
async def create_user_role(user_role: UserRole):
    return await user_role.create()

@router.get("/", response_model=List[UserRole])
async def read_user_roles():
    return await UserRole.read_all()

@router.get("/{user_role_id}", response_model=UserRole)
async def read_user_role(user_role_id: int):
    user_role = await UserRole.read(user_role_id)
    if user_role is None:
        raise HTTPException(status_code=404, detail="User Role not found")
    return user_role

@router.put("/{user_role_id}", response_model=UserRole)
async def update_user_role(user_role_id: int, user_role: UserRole):
    return await user_role.update(user_role_id)

@router.delete("/{user_role_id}")
async def delete_user_role(user_role_id: int):
    return await user_role.delete(user_role_id)
