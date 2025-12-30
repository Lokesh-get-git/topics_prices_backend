from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db import Base

class PremiumTopicAdjustment(Base):
    __tablename__ = "premium_topic_adjustments"

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    interview_type = Column(String(30), nullable=False)  
    adjustment_percentage = Column(Numeric(8, 2), default=0)  
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    topic = relationship("Topic", back_populates="adjustments",passive_deletes=True)
