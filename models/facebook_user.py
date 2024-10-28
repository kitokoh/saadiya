from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class FacebookUser(Base):
    __tablename__ = 'facebook_users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    facebook_id = Column(String, unique=True)

# CRUD Operations
def create_facebook_user(db, name, facebook_id):
    new_facebook_user = FacebookUser(name=name, facebook_id=facebook_id)
    db.add(new_facebook_user)
    db.commit()
    db.refresh(new_facebook_user)
    return new_facebook_user

def read_facebook_user(db, facebook_user_id):
    return db.query(FacebookUser).filter(FacebookUser.id == facebook_user_id).first()

def update_facebook_user(db, facebook_user_id, name=None):
    facebook_user = db.query(FacebookUser).filter(FacebookUser.id == facebook_user_id).first()
    if facebook_user:
        if name:
            facebook_user.name = name
        db.commit()
        db.refresh(facebook_user)
    return facebook_user

def delete_facebook_user(db, facebook_user_id):
    facebook_user = db.query(FacebookUser).filter(FacebookUser.id == facebook_user_id).first()
    if facebook_user:
        db.delete(facebook_user)
        db.commit()
