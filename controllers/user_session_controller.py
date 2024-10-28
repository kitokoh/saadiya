# user_session_controller.py
from fastapi import APIRouter, HTTPException
from models.user_session import UserSession
from typing import List

router = APIRouter()

@router.post("/", response_model=UserSession)
async def create_user_session(user_session: UserSession):
    return await user_session.create()

@router.get("/", response_model=List[UserSession])
async def read_user_sessions():
    return await UserSession.read_all()

@router.get("/{user_session_id}", response_model=UserSession)
async def read_user_session(user_session_id: int):
    user_session = await UserSession.read(user_session_id)
    if user_session is None:
        raise HTTPException(status_code=404, detail="User Session not found")
    return user_session

@router.put("/{user_session_id}", response_model=UserSession)
async def update_user_session(user_session_id: int, user_session: UserSession):
    return await user_session.update(user_session_id)

@router.delete("/{user_session_id}")
async def delete_user_session(user_session_id: int):
    return await user_session.delete(user_session_id)
