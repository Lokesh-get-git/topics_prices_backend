from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from db import Base

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    classification = Column(String(20), nullable=False)
    description = Column(Text, nullable=False)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    display_names = relationship("TopicDisplayName", back_populates="topic", cascade="all, delete-orphan")
    keywords = relationship("TopicKeyword", back_populates="topic", cascade="all, delete-orphan")
    experience_ranges = relationship("TopicExperienceRange", back_populates="topic", cascade="all, delete-orphan")
    adjustments = relationship("PremiumTopicAdjustment", back_populates="topic", cascade="all, delete-orphan")


class TopicDisplayName(Base):
    __tablename__ = "topic_display_names"

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    topic = relationship("Topic", back_populates="display_names")


class TopicKeyword(Base):
    __tablename__ = "topic_keywords"

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    keyword = Column(String(50), nullable=False)
    topic = relationship("Topic", back_populates="keywords")
