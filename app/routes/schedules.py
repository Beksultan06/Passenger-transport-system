from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import SessionLocal
from app.db.models.schedule import Schedule
from app.db.schemas.schedule import ScheduleCreate, ScheduleResponse, ScheduleUpdate
from app.services.notification import send_notification, send_email_notification, send_telegram_notification

router = APIRouter()


# Получение сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Создать новое расписание и отправить уведомления
@router.post("/", response_model=ScheduleResponse)
def create_schedule(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    new_schedule = Schedule(**schedule.dict())
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)

    # Отправка уведомления водителю о новом рейсе
    message = f"Вам назначен новый рейс на {new_schedule.date} в {new_schedule.departure_time}"
    send_notification(new_schedule.driver_id, message)
    send_email_notification("driver_email@example.com", "Новый рейс", message)
    send_telegram_notification("123456789", message)

    return new_schedule


# Обновить расписание и уведомить водителя
@router.put("/{schedule_id}", response_model=ScheduleResponse)
def update_schedule(schedule_id: int, schedule_data: ScheduleUpdate, db: Session = Depends(get_db)):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Расписание не найдено")

    for key, value in schedule_data.dict(exclude_unset=True).items():
        setattr(schedule, key, value)

    db.commit()
    db.refresh(schedule)

    # Отправка уведомления об изменении рейса
    message = f"Ваш рейс на {schedule.date} был обновлён. Новое время: {schedule.departure_time}"
    send_notification(schedule.driver_id, message)
    send_email_notification("driver_email@example.com", "Обновление рейса", message)
    send_telegram_notification("123456789", message)

    return schedule
