from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from app.core.database import Base


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)

    station_code = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    station_name = Column(String)

    latitude = Column(Float)
    longitude = Column(Float)

    elevation = Column(Float, nullable=True)

    state = Column(String, nullable=True)
    district = Column(String, nullable=True)

    status = Column(
        String,
        default="active"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )