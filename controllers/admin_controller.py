# admin_controller.py
from fastapi import APIRouter, HTTPException
from models.admin import Admin
from typing import List

router = APIRouter()

@router.post("/", response_model=Admin)
async def create_admin(admin: Admin):
    return await admin.create()

@router.get("/", response_model=List[Admin])
async def read_admins():
    return await Admin.read_all()

@router.get("/{admin_id}", response_model=Admin)
async def read_admin(admin_id: int):
    admin = await Admin.read(admin_id)
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin

@router.put("/{admin_id}", response_model=Admin)
async def update_admin(admin_id: int, admin: Admin):
    return await admin.update(admin_id)

@router.delete("/{admin_id}")
async def delete_admin(admin_id: int):
    return await admin.delete(admin_id)
