from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db import Base

class ExperienceRange(Base):
    __tablename__ = "experience_ranges"

    id = Column(Integer, primary_key=True)
    label = Column(String(50), nullable=False) 
    sort_order = Column(Integer, nullable=False)

    base_pricing = relationship("BasePricing", back_populates="experience_range")
    topic_ranges = relationship("TopicExperienceRange", back_populates="experience_range", cascade="all, delete-orphan",passive_deletes=True)


class TopicExperienceRange(Base):
    __tablename__ = "topic_experience_ranges"

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    experience_range_id = Column(Integer, ForeignKey("experience_ranges.id",ondelete="CASCADE"), nullable=False)
    
    topic = relationship("Topic", back_populates="experience_ranges",passive_deletes=True)
    experience_range = relationship("ExperienceRange", back_populates="topic_ranges")
