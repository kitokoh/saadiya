# group_controller.py
from fastapi import APIRouter, HTTPException
from models.group import Group
from typing import List

router = APIRouter()

@router.post("/", response_model=Group)
async def create_group(group: Group):
    return await group.create()

@router.get("/", response_model=List[Group])
async def read_groups():
    return await Group.read_all()

@router.get("/{group_id}", response_model=Group)
async def read_group(group_id: int):
    group = await Group.read(group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.put("/{group_id}", response_model=Group)
async def update_group(group_id: int, group: Group):
    return await group.update(group_id)

@router.delete("/{group_id}")
async def delete_group(group_id: int):
    return await group.delete(group_id)
