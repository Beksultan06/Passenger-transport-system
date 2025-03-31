from sqlalchemy import Column, Integer, String, Enum
from app.db.database import Base
import enum

class RoleEnum(str, enum.Enum):
    driver = "driver"
    dispatcher = "dispatcher"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.driver)