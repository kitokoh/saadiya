# backup_log_controller.py
from fastapi import APIRouter, HTTPException
from models.backup_log import BackupLog
from typing import List

router = APIRouter()

@router.post("/", response_model=BackupLog)
async def create_backup_log(backup_log: BackupLog):
    return await backup_log.create()

@router.get("/", response_model=List[BackupLog])
async def read_backup_logs():
    return await BackupLog.read_all()

@router.get("/{backup_log_id}", response_model=BackupLog)
async def read_backup_log(backup_log_id: int):
    backup_log = await BackupLog.read(backup_log_id)
    if backup_log is None:
        raise HTTPException(status_code=404, detail="Backup Log not found")
    return backup_log

@router.put("/{backup_log_id}", response_model=BackupLog)
async def update_backup_log(backup_log_id: int, backup_log: BackupLog):
    return await backup_log.update(backup_log_id)

@router.delete("/{backup_log_id}")
async def delete_backup_log(backup_log_id: int):
    return await backup_log.delete(backup_log_id)
