# from sqlalchemy import Column, Integer, String
# from database import Base

# class Quota(Base):
#     __tablename__ = 'quotas'

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer)
#     limit = Column(Integer)

# # CRUD Operations
# def create_quota(db, user_id, limit):
#     new_quota = Quota(user_id=user_id, limit=limit)
#     db.add(new_quota)
#     db.commit()
#     db.refresh(new_quota)
#     return new_quota

# def read_quota(db, quota_id):
#     return db.query(Quota).filter(Quota.id == quota_id).first()

# def update_quota(db, quota_id, limit=None):
#     quota = db.query(Quota).filter(Quota.id == quota_id).first()
#     if quota:
#         if limit is not None:
#             quota.limit = limit
#         db.commit()
#         db.refresh(quota)
#     return quota

# def delete_quota(db, quota_id):
#     quota = db.query(Quota).filter(Quota.id == quota_id).first()
#     if quota:
#         db.delete(quota)
#         db.commit()
# models/quota.py
from sqlalchemy import Column, Integer, String
from database import Base

class Quota(Base):
    __tablename__ = "quotas"

    id = Column(Integer, primary_key=True, index=True)
    limit = Column(Integer)
    used = Column(Integer)
