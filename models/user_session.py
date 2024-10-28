# from sqlalchemy import Column, Integer, String, DateTime
# from datetime import datetime
# from database import Base

# class UserSession(Base):
#     __tablename__ = 'user_sessions'

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer)
#     session_token = Column(String)
#     created_at = Column(DateTime, default=datetime.utcnow)

# # CRUD Operations
# def create_user_session(db, user_id, session_token):
#     new_user_session = UserSession(user_id=user_id, session_token=session_token)
#     db.add(new_user_session)
#     db.commit()
#     db.refresh(new_user_session)
#     return new_user_session

# def read_user_session(db, session_id):
#     return db.query(UserSession).filter(UserSession.id == session_id).first()

# def delete_user_session(db, session_id):
#     user_session = db.query(UserSession).filter(UserSession.id == session_id).first()
#     if user_session:
#         db.delete(user_session)
#         db.commit()
# models/user_session.py
from sqlalchemy import Column, Integer, String
from database import Base

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String)
    user_id = Column(Integer)
