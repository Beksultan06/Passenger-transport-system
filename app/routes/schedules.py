from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.database import SessionLocal
from app.services.scheduler import generate_schedule_for_week

router = APIRouter()

# Получение сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Автоматическое создание расписания на неделю
@router.post("/generate/")
def auto_generate_schedule(start_date: str, db: Session = Depends(get_db)):
    try:
        parsed_date = datetime.strptime(start_date, "%Y-%m-%d")
        schedules = generate_schedule_for_week(db, parsed_date, interval_minutes=60)
        return {"message": "Расписание успешно создано", "schedules_count": len(schedules)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
