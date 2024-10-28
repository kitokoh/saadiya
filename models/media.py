from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    url = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="media")

# CRUD Operations
def create_media(db, media_type, url, user_id):
    new_media = Media(type=media_type, url=url, user_id=user_id)
    db.add(new_media)
    db.commit()
    db.refresh(new_media)
    return new_media

def read_media(db, media_id):
    return db.query(Media).filter(Media.id == media_id).first()

def update_media(db, media_id, media_type=None, url=None):
    media = db.query(Media).filter(Media.id == media_id).first()
    if media:
        if media_type:
            media.type = media_type
        if url:
            media.url = url
        db.commit()
        db.refresh(media)
    return media

def delete_media(db, media_id):
    media = db.query(Media).filter(Media.id == media_id).first()
    if media:
        db.delete(media)
        db.commit()
