from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

# Хранилище для подключённых клиентов WebSocket
connected_clients: Dict[int, WebSocket] = {}


# Подключение нового клиента
async def connect_client(websocket: WebSocket, user_id: int):
    await websocket.accept()
    connected_clients[user_id] = websocket


# Отключение клиента
def disconnect_client(user_id: int):
    if user_id in connected_clients:
        del connected_clients[user_id]


# Отправка уведомления через WebSocket
async def send_notification(user_id: int, message: str):
    if user_id in connected_clients:
        websocket = connected_clients[user_id]
        await websocket.send_text(message)


# Отправка email уведомления
def send_email_notification(to_email: str, subject: str, message: str):
    try:
        msg = MIMEText(message, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = settings.EMAIL_FROM
        msg["To"] = to_email

        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_FROM, settings.EMAIL_PASSWORD)
            server.sendmail(settings.EMAIL_FROM, to_email, msg.as_string())
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")


# Отправка уведомления в Telegram
def send_telegram_notification(chat_id: str, message: str):
    import requests

    telegram_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}

    response = requests.post(telegram_url, json=payload)
    if response.status_code != 200:
        print(f"Ошибка отправки сообщения в Telegram: {response.text}")
