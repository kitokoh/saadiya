# alert_controller.py
from fastapi import APIRouter, HTTPException
from models.alert import Alert
from typing import List

router = APIRouter()

@router.post("/", response_model=Alert)
async def create_alert(alert: Alert):
    return await alert.create()

@router.get("/", response_model=List[Alert])
async def read_alerts():
    return await Alert.read_all()

@router.get("/{alert_id}", response_model=Alert)
async def read_alert(alert_id: int):
    alert = await Alert.read(alert_id)
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.put("/{alert_id}", response_model=Alert)
async def update_alert(alert_id: int, alert: Alert):
    return await alert.update(alert_id)

@router.delete("/{alert_id}")
async def delete_alert(alert_id: int):
    return await alert.delete(alert_id)
