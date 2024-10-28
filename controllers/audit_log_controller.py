# audit_log_controller.py
from fastapi import APIRouter, HTTPException
from models.audit_log import AuditLog
from typing import List

router = APIRouter()

@router.post("/", response_model=AuditLog)
async def create_audit_log(audit_log: AuditLog):
    return await audit_log.create()

@router.get("/", response_model=List[AuditLog])
async def read_audit_logs():
    return await AuditLog.read_all()

@router.get("/{audit_log_id}", response_model=AuditLog)
async def read_audit_log(audit_log_id: int):
    audit_log = await AuditLog.read(audit_log_id)
    if audit_log is None:
        raise HTTPException(status_code=404, detail="Audit Log not found")
    return audit_log

@router.put("/{audit_log_id}", response_model=AuditLog)
async def update_audit_log(audit_log_id: int, audit_log: AuditLog):
    return await audit_log.update(audit_log_id)

@router.delete("/{audit_log_id}")
async def delete_audit_log(audit_log_id: int):
    return await audit_log.delete(audit_log_id)
