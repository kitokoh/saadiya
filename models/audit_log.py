# from sqlalchemy import Column, Integer, String, DateTime
# from datetime import datetime
# from database import Base

# class AuditLog(Base):
#     __tablename__ = 'audit_logs'

#     id = Column(Integer, primary_key=True, index=True)
#     action = Column(String)
#     timestamp = Column(DateTime, default=datetime.utcnow)
#     user_id = Column(Integer)

# # CRUD Operations
# def create_audit_log(db, action, user_id):
#     new_audit_log = AuditLog(action=action, user_id=user_id)
#     db.add(new_audit_log)
#     db.commit()
#     db.refresh(new_audit_log)
#     return new_audit_log

# def read_audit_log(db, log_id):
#     return db.query(AuditLog).filter(AuditLog.id == log_id).first()

# def delete_audit_log(db, log_id):
#     log = db.query(AuditLog).filter(AuditLog.id == log_id).first()
#     if log:
#         db.delete(log)
#         db.commit()
# models/audit_log.py
from sqlalchemy import Column, Integer, String
from database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String)
    timestamp = Column(String)
