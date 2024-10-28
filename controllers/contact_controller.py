# contact_controller.py
from fastapi import APIRouter, HTTPException
from models.contact import Contact
from typing import List

router = APIRouter()

@router.post("/", response_model=Contact)
async def create_contact(contact: Contact):
    return await contact.create()

@router.get("/", response_model=List[Contact])
async def read_contacts():
    return await Contact.read_all()

@router.get("/{contact_id}", response_model=Contact)
async def read_contact(contact_id: int):
    contact = await Contact.read(contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=Contact)
async def update_contact(contact_id: int, contact: Contact):
    return await contact.update(contact_id)

@router.delete("/{contact_id}")
async def delete_contact(contact_id: int):
    return await contact.delete(contact_id)
