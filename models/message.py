# models/message.py
from database import Base
from sqlalchemy import Column, Integer, String


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
