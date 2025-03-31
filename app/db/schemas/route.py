from pydantic import BaseModel, constr, conint
from typing import List, Optional


# Схема для маршрута
class RouteBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=3, max_length=100)
    start_point: str
    end_point: str
    distance_km: conint(gt=0)


# Схема для создания маршрута
class RouteCreate(RouteBase):
    pass


# Схема для обновления маршрута
class RouteUpdate(BaseModel):
    name: Optional[str]
    start_point: Optional[str]
    end_point: Optional[str]
    distance_km: Optional[int]


# Схема для ответа
class RouteResponse(RouteBase):
    id: int

    class Config:
        orm_mode = True
