# instance_user_controller.py
from fastapi import APIRouter, HTTPException
from models.instance_user import InstanceUser
from typing import List

router = APIRouter()

@router.post("/", response_model=InstanceUser)
async def create_instance_user(instance_user: InstanceUser):
    return await instance_user.create()

@router.get("/", response_model=List[InstanceUser])
async def read_instance_users():
    return await InstanceUser.read_all()

@router.get("/{instance_user_id}", response_model=InstanceUser)
async def read_instance_user(instance_user_id: int):
    instance_user = await InstanceUser.read(instance_user_id)
    if instance_user is None:
        raise HTTPException(status_code=404, detail="Instance User not found")
    return instance_user

@router.put("/{instance_user_id}", response_model=InstanceUser)
async def update_instance_user(instance_user_id: int, instance_user: InstanceUser):
    return await instance_user.update(instance_user_id)

@router.delete("/{instance_user_id}")
async def delete_instance_user(instance_user_id: int):
    return await instance_user.delete(instance_user_id)

