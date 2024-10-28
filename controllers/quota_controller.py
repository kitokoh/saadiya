# quota_controller.py
from fastapi import APIRouter, HTTPException
from models.quota import Quota
from typing import List

router = APIRouter()

@router.post("/", response_model=Quota)
async def create_quota(quota: Quota):
    return await quota.create()

@router.get("/", response_model=List[Quota])
async def read_quotas():
    return await Quota.read_all()

@router.get("/{quota_id}", response_model=Quota)
async def read_quota(quota_id: int):
    quota = await Quota.read(quota_id)
    if quota is None:
        raise HTTPException(status_code=404, detail="Quota not found")
    return quota

@router.put("/{quota_id}", response_model=Quota)
async def update_quota(quota_id: int, quota: Quota):
    return await quota.update(quota_id)

@router.delete("/{quota_id}")
async def delete_quota(quota_id: int):
    return await quota.delete(quota_id)
