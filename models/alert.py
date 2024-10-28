from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    message = Column(String)
    is_read = Column(Boolean, default=False)

# CRUD Operations
def create_alert(db, user_id, message):
    new_alert = Alert(user_id=user_id, message=message)
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    return new_alert

def read_alert(db, alert_id):
    return db.query(Alert).filter(Alert.id == alert_id).first()

def update_alert(db, alert_id, is_read=None):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        if is_read is not None:
            alert.is_read = is_read
        db.commit()
        db.refresh(alert)
    return alert

def delete_alert(db, alert_id):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        db.delete(alert)
        db.commit()
