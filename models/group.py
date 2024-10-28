from sqlalchemy import Column, Integer, String
from database import Base

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

# CRUD Operations
def create_group(db, name, description):
    new_group = Group(name=name, description=description)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

def read_group(db, group_id):
    return db.query(Group).filter(Group.id == group_id).first()

def update_group(db, group_id, name=None, description=None):
    group = db.query(Group).filter(Group.id == group_id).first()
    if group:
        if name:
            group.name = name
        if description:
            group.description = description
        db.commit()
        db.refresh(group)
    return group

def delete_group(db, group_id):
    group = db.query(Group).filter(Group.id == group_id).first()
    if group:
        db.delete(group)
        db.commit()
