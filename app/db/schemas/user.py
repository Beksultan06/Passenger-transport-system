from pydantic import BaseModel, EmailStr
from typing import Optional
import enum


class RoleEnum(str, enum.Enum):
    driver = "driver"
    dispatcher = "dispatcher"
    admin = "admin"


# Схема для отображения данных пользователя
class UserBase(BaseModel):
    full_name: str
    phone: str
    role: RoleEnum


# Схема для создания нового пользователя
class UserCreate(UserBase):
    password: str


# Схема для ответа при аутентификации
class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


# Схема для аутентификации
class UserLogin(BaseModel):
    phone: str
    password: str


# Схема для обновления информации о пользователе
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
