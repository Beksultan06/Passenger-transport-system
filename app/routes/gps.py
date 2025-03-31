from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models.location import Location
from datetime import datetime

router = APIRouter()

# Хранилище активных подключений WebSocket
connected_clients = {}


# Получение сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Получение данных о GPS через WebSocket
@router.websocket("/ws/gps/{driver_id}")
async def websocket_gps_endpoint(websocket: WebSocket, driver_id: int):
    await websocket.accept()
    connected_clients[driver_id] = websocket
    try:
        while True:
            data = await websocket.receive_json()
            latitude = data.get("latitude")
            longitude = data.get("longitude")

            if latitude and longitude:
                save_driver_location(driver_id, latitude, longitude)
                await broadcast_location(driver_id, latitude, longitude)

    except WebSocketDisconnect:
        del connected_clients[driver_id]


# Сохранение координат водителя в БД
def save_driver_location(driver_id: int, latitude: float, longitude: float, db: Session = next(get_db())):
    location = Location(
        driver_id=driver_id,
        latitude=latitude,
        longitude=longitude,
        timestamp=datetime.utcnow(),
    )
    db.add(location)
    db.commit()


# Рассылка координат всем клиентам
async def broadcast_location(driver_id: int, latitude: float, longitude: float):
    for client in connected_clients.values():
        await client.send_json(
            {"driver_id": driver_id, "latitude": latitude, "longitude": longitude}
        )
