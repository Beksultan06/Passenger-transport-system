from pydantic import BaseModel
from datetime import datetime


# Схема для отправки координат
class LocationBase(BaseModel):
    driver_id: int
    latitude: float
    longitude: float


# Схема для создания локации
class LocationCreate(LocationBase):
    pass


# Схема для ответа
class LocationResponse(LocationBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
