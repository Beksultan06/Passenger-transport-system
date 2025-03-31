from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import SessionLocal
from app.db.models.schedule import Schedule
from app.db.schemas.schedule import ScheduleCreate, ScheduleResponse, ScheduleUpdate
from app.bot import notify_driver

router = APIRouter()


# Получение сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Создать новое расписание и уведомить водителя
@router.post("/", response_model=ScheduleResponse)
async def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    new_schedule = Schedule(**schedule.dict())
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)

    # Отправка уведомления водителю о новом рейсе
    message = (
        f"🚍 Вам назначен новый рейс!\n"
        f"📅 Дата: {new_schedule.date}\n"
        f"⏰ Время: {new_schedule.departure_time} - {new_schedule.return_time}"
    )
    await notify_driver(new_schedule.driver_id, message)

    return new_schedule
