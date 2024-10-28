from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class InstanceUser(Base):
    __tablename__ = 'instance_users'

    id = Column(Integer, primary_key=True, index=True)
    instance_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="instances")

# CRUD Operations
def create_instance_user(db, instance_id, user_id):
    new_instance_user = InstanceUser(instance_id=instance_id, user_id=user_id)
    db.add(new_instance_user)
    db.commit()
    db.refresh(new_instance_user)
    return new_instance_user

def read_instance_user(db, instance_user_id):
    return db.query(InstanceUser).filter(InstanceUser.id == instance_user_id).first()

def delete_instance_user(db, instance_user_id):
    instance_user = db.query(InstanceUser).filter(InstanceUser.id == instance_user_id).first()
    if instance_user:
        db.delete(instance_user)
        db.commit()
