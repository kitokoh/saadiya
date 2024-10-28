# from sqlalchemy import Column, Integer, String, DateTime
# from datetime import datetime
# from database import Base

# class BackupLog(Base):
#     __tablename__ = 'backup_logs'

#     id = Column(Integer, primary_key=True, index=True)
#     backup_time = Column(DateTime, default=datetime.utcnow)
#     status = Column(String)

# # CRUD Operations
# def create_backup_log(db, status):
#     new_backup_log = BackupLog(status=status)
#     db.add(new_backup_log)
#     db.commit()
#     db.refresh(new_backup_log)
#     return new_backup_log

# def read_backup_log(db, backup_id):
#     return db.query(BackupLog).filter(BackupLog.id == backup_id).first()

# def delete_backup_log(db, backup_id):
#     backup_log = db.query(BackupLog).filter(BackupLog.id == backup_id).first()
#     if backup_log:
#         db.delete(backup_log)
#         db.commit()
# models/backup_log.py
from sqlalchemy import Column, Integer, String
from database import Base

class BackupLog(Base):
    __tablename__ = "backup_logs"

    id = Column(Integer, primary_key=True, index=True)
    backup_time = Column(String)
    status = Column(String)
