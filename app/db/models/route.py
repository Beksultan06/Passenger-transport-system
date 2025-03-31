from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    start_point = Column(String, nullable=False)
    end_point = Column(String, nullable=False)
    distance_km = Column(Integer)

    schedules = relationship("Schedule", back_populates="route")