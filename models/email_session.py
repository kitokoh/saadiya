# from sqlalchemy import Column, Integer, String, DateTime
# from datetime import datetime
# from database import Base

# class EmailSession(Base):
#     __tablename__ = 'email_sessions'

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer)
#     session_token = Column(String)
#     created_at = Column(DateTime, default=datetime.utcnow)

# # CRUD Operations
# def create_email_session(db, user_id, session_token):
#     new_email_session = EmailSession(user_id=user_id, session_token=session_token)
#     db.add(new_email_session)
#     db.commit()
#     db.refresh(new_email_session)
#     return new_email_session

# def read_email_session(db, session_id):
#     return db.query(EmailSession).filter(EmailSession.id == session_id).first()

# def delete_email_session(db, session_id):
#     email_session = db.query(EmailSession).filter(EmailSession.id == session_id).first()
#     if email_session:
#         db.delete(email_session)
#         db.commit()
# models/email_session.py
from sqlalchemy import Column, Integer, String
from database import Base

class EmailSession(Base):
    __tablename__ = "email_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String)
    user_id = Column(Integer)
