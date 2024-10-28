# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from database import Base

# class UserRole(Base):
#     __tablename__ = 'user_roles'

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     role = Column(String)

#     user = relationship("User", back_populates="roles")

# # CRUD Operations
# def create_user_role(db, user_id, role):
#     new_user_role = UserRole(user_id=user_id, role=role)
#     db.add(new_user_role)
#     db.commit()
#     db.refresh(new_user_role)
#     return new_user_role

# def read_user_role(db, role_id):
#     return db.query(UserRole).filter(UserRole.id == role_id).first()

# def update_user_role(db, role_id, role=None):
#     user_role = db.query(UserRole).filter(UserRole.id == role_id).first()
#     if user_role:
#         if role:
#             user_role.role = role
#         db.commit()
#         db.refresh(user_role)
#     return user_role

# def delete_user_role(db, role_id):
#     user_role = db.query(UserRole).filter(UserRole.id == role_id).first()
#     if user_role:
#         db.delete(user_role)
#         db.commit()
from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from database import Base

# class UserRole(Base):
#     __tablename__ = 'user_roles'

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     role = Column(String)

#     user = relationship("User", back_populates="roles")

# # CRUD Operations
# def create_user_role(db, user_id, role):
#     new_user_role = UserRole(user_id=user_id, role=role)
#     db.add(new_user_role)
#     db.commit()
#     db.refresh(new_user_role)
#     return new_user_role

# def read_user_role(db, role_id):
#     return db.query(UserRole).filter(UserRole.id == role_id).first()

# def update_user_role(db, role_id, role=None):
#     user_role = db.query(UserRole).filter(UserRole.id == role_id).first()
#     if user_role:
#         if role:
#             user_role.role = role
#         db.commit()
#         db.refresh(user_role)
#     return user_role

# def delete_user_role(db, role_id):
#     user_role = db.query(UserRole).filter(UserRole.id == role_id).first()
#     if user_role:
#         db.delete(user_role)
#         db.commit()
# models/user_role.py
from sqlalchemy import Column, Integer, String
from database import Base

class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    role_id = Column(Integer)
