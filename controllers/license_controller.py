# instance_controller.py
from fastapi import APIRouter, HTTPException
from models.instance import Instance
from typing import List

router = APIRouter()

@router.post("/", response_model=Instance)
async def create_instance(instance: Instance):
    return await instance.create()

@router.get("/", response_model=List[Instance])
async def read_instances():
    return await Instance.read_all()

@router.get("/{instance_id}", response_model=Instance)
async def read_instance(instance_id: int):
    instance = await Instance.read(instance_id)
    if instance is None:
        raise HTTPException(status_code=404, detail="Instance not found")
    return instance

@router.put("/{instance_id}", response_model=Instance)
async def update_instance(instance_id: int, instance: Instance):
    return await instance.update(instance_id)

@router.delete("/{instance_id}")
async def delete_instance(instance_id: int):
    return await instance.delete(instance_id)
