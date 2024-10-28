# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from database import Base

# class GroupUser(Base):
#     __tablename__ = 'group_users'

#     id = Column(Integer, primary_key=True, index=True)
#     group_id = Column(Integer)
#     user_id = Column(Integer, ForeignKey('users.id'))

#     user = relationship("User", back_populates="groups")

# # CRUD Operations
# def create_group_user(db, group_id, user_id):
#     new_group_user = GroupUser(group_id=group_id, user_id=user_id)
#     db.add(new_group_user)
#     db.commit()
#     db.refresh(new_group_user)
#     return new_group_user

# def read_group_user(db, group_user_id):
#     return db.query(GroupUser).filter(GroupUser.id == group_user_id).first()

# def delete_group_user(db, group_user_id):
#     group_user = db.query(GroupUser).filter(GroupUser.id == group_user_id).first()
#     if group_user:
#         db.delete(group_user)
#         db.commit()
# models/group_user.py
from sqlalchemy import Column, Integer, String
from database import Base

class GroupUser(Base):
    __tablename__ = "group_users"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer)
    user_id = Column(Integer)
