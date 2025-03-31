from pydantic import BaseModel
from datetime import date, time
from typing import Optional


# Схема для создания расписания
class ScheduleBase(BaseModel):
    route_id: int
    driver_id: int
    departure_time: time
    return_time: Optional[time]
    date: date


# Схема для создания расписания
class ScheduleCreate(ScheduleBase):
    pass


# Схема для обновления расписания
class ScheduleUpdate(BaseModel):
    route_id: Optional[int]
    driver_id: Optional[int]
    departure_time: Optional[time]
    return_time: Optional[time]
    date: Optional[date]


# Схема для ответа
class ScheduleResponse(ScheduleBase):
    id: int

    class Config:
        orm_mode = True
