# email_session_controller.py
from fastapi import APIRouter, HTTPException
from models.email_session import EmailSession
from typing import List

router = APIRouter()

@router.post("/", response_model=EmailSession)
async def create_email_session(email_session: EmailSession):
    return await email_session.create()

@router.get("/", response_model=List[EmailSession])
async def read_email_sessions():
    return await EmailSession.read_all()

@router.get("/{email_session_id}", response_model=EmailSession)
async def read_email_session(email_session_id: int):
    email_session = await EmailSession.read(email_session_id)
    if email_session is None:
        raise HTTPException(status_code=404, detail="Email Session not found")
    return email_session

@router.put("/{email_session_id}", response_model=EmailSession)
async def update_email_session(email_session_id: int, email_session: EmailSession):
    return await email_session.update(email_session_id)

@router.delete("/{email_session_id}")
async def delete_email_session(email_session_id: int):
    return await email_session.delete(email_session_id)
