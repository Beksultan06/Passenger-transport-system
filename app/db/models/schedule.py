from sqlalchemy import Column, Integer, Time, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
    driver_id = Column(Integer, ForeignKey("users.id"))
    departure_time = Column(Time, nullable=False)
    return_time = Column(Time)
    date = Column(Date)

    route = relationship("Route", back_populates="schedules")