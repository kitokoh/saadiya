# role_controller.py
from fastapi import APIRouter, HTTPException
from models.role import Role
from typing import List

router = APIRouter()

@router.post("/", response_model=Role)
async def create_role(role: Role):
    return await role.create()

@router.get("/", response_model=List[Role])
async def read_roles():
    return await Role.read_all()

@router.get("/{role_id}", response_model=Role)
async def read_role(role_id: int):
    role = await Role.read(role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.put("/{role_id}", response_model=Role)
async def update_role(role_id: int, role: Role):
    return await role.update(role_id)

@router.delete("/{role_id}")
async def delete_role(role_id: int):
    return await role.delete(role_id)
