from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.notification import connect_client, disconnect_client, send_notification

router = APIRouter()

# Подключение WebSocket для водителей и диспетчеров
@router.websocket("/ws/notifications/{user_id}")
async def websocket_notifications(websocket: WebSocket, user_id: int):
    await connect_client(websocket, user_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        disconnect_client(user_id)
