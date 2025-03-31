from sqlalchemy.orm import Session
from datetime import datetime, timedelta, time
from app.db.models.schedule import Schedule
from app.db.models.route import Route
from app.db.models.user import User


# Автоматическое составление расписания на неделю
def generate_schedule_for_week(db: Session, start_date: datetime, interval_minutes: int = 60):
    routes = db.query(Route).all()
    drivers = db.query(User).filter(User.role == "driver").all()

    if not routes or not drivers:
        raise Exception("Не найдены маршруты или доступные водители")

    current_date = start_date
    schedules = []

    for i in range(7):  # Создаем расписание на 7 дней
        for route in routes:
            available_driver = get_available_driver(route.id, current_date, db, drivers)

            if available_driver:
                departure_time = time(8, 0)  # Начало в 08:00
                return_time = calculate_return_time(departure_time, interval_minutes)

                schedule = Schedule(
                    route_id=route.id,
                    driver_id=available_driver.id,
                    departure_time=departure_time,
                    return_time=return_time,
                    date=current_date.date(),
                )
                schedules.append(schedule)
                db.add(schedule)

        current_date += timedelta(days=1)

    db.commit()
    return schedules


# Получить доступного водителя для маршрута
def get_available_driver(route_id: int, date: datetime, db: Session, drivers: list):
    assigned_driver_ids = (
        db.query(Schedule.driver_id)
        .filter(Schedule.route_id == route_id, Schedule.date == date.date())
        .all()
    )

    assigned_driver_ids = [id[0] for id in assigned_driver_ids]
    available_drivers = [driver for driver in drivers if driver.id not in assigned_driver_ids]

    if available_drivers:
        return available_drivers[0]  # Назначаем первого доступного водителя
    return None


# Рассчитать время обратного рейса
def calculate_return_time(departure_time: time, interval_minutes: int) -> time:
    departure_dt = datetime.combine(datetime.today(), departure_time)
    return_dt = departure_dt + timedelta(minutes=interval_minutes)
    return return_dt.time()
