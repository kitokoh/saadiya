# message_controller.py
from fastapi import APIRouter, HTTPException
from models.message import Message
from typing import List

router = APIRouter()

@router.post("/", response_model=Message)
async def create_message(message: Message):
    return await message.create()

@router.get("/", response_model=List[Message])
async def read_messages():
    return await Message.read_all()

@router.get("/{message_id}", response_model=Message)
async def read_message(message_id: int):
    message = await Message.read(message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@router.put("/{message_id}", response_model=Message)
async def update_message(message_id: int, message: Message):
    return await message.update(message_id)

@router.delete("/{message_id}")
async def delete_message(message_id: int):
    return await message.delete(message_id)
