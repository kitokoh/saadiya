# from sqlalchemy import Column, Integer, String
# from database import Base

# class Contact(Base):
#     __tablename__ = 'contacts'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     email = Column(String)
#     phone = Column(String)

# # CRUD Operations
# def create_contact(db, name, email, phone):
#     new_contact = Contact(name=name, email=email, phone=phone)
#     db.add(new_contact)
#     db.commit()
#     db.refresh(new_contact)
#     return new_contact

# def read_contact(db, contact_id):
#     return db.query(Contact).filter(Contact.id == contact_id).first()

# def update_contact(db, contact_id, name=None, email=None, phone=None):
#     contact = db.query(Contact).filter(Contact.id == contact_id).first()
#     if contact:
#         if name:
#             contact.name = name
#         if email:
#             contact.email = email
#         if phone:
#             contact.phone = phone
#         db.commit()
#         db.refresh(contact)
#     return contact

# def delete_contact(db, contact_id):
#     contact = db.query(Contact).filter(Contact.id == contact_id).first()
#     if contact:
#         db.delete(contact)
#         db.commit()
# models/contact.py
from sqlalchemy import Column, Integer, String
from database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    message = Column(String)
