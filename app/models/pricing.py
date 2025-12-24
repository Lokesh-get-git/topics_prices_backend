from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db import Base

class BasePricing(Base):
    __tablename__ = "base_pricing"

    id = Column(Integer, primary_key=True)
    classification = Column(String(20), nullable=False)
    interview_type = Column(String(30), nullable=False)
    experience_level_id = Column(Integer, ForeignKey("experience_ranges.id"), nullable=False)
    duration_mins = Column(Integer, nullable=True) 
    domestic_price = Column(Numeric(10, 2), nullable=False)
    international_price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    experience_range = relationship("ExperienceRange", back_populates="base_pricing")
