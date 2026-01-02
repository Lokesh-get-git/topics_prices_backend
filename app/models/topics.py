from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime,ForeignKey, func
from sqlalchemy.dialects.postgresql import ARRAY,UUID
import uuid
from sqlalchemy.orm import relationship
from app.db import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False)
    classification = Column(String(20), nullable=False)
    description = Column(Text, nullable=False)
    published = Column(Boolean, default=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    display_names = Column(ARRAY(String), nullable=False)

    keywords = relationship(
        "Keyword",
        secondary="topic_keywords",
        back_populates="topics",
        passive_deletes=True
    )

    experience_ranges = relationship("TopicExperienceRange", back_populates="topic", cascade="all, delete-orphan",passive_deletes=True)
    
    adjustments = relationship("PremiumTopicAdjustment", back_populates="topic", cascade="all, delete-orphan",passive_deletes=True)


class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), unique=True, nullable=False)

    topics = relationship(
        "Topic",
        secondary="topic_keywords",
        back_populates="keywords"
    )

class TopicKeyword(Base):
    __tablename__ = "topic_keywords"

    topic_id = Column(
        UUID(as_uuid=True),
        ForeignKey("topics.id", ondelete="CASCADE"),
        primary_key=True
    )
    keyword_id = Column(
        Integer,
        ForeignKey("keywords.id", ondelete="CASCADE"),
        primary_key=True
    )

