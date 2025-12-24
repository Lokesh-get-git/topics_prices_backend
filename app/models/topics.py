from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime,ForeignKey, func
from sqlalchemy.orm import relationship
from app.db import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    classification = Column(String(20), nullable=False)
    description = Column(Text, nullable=False)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    display_names = relationship(
        "DisplayName",
        secondary="topic_display_names",
        back_populates="topics"
    )

    keywords = relationship(
        "Keyword",
        secondary="topic_keywords",
        back_populates="topics"
    )

    experience_ranges = relationship("TopicExperienceRange", back_populates="topic", cascade="all, delete-orphan")
    adjustments = relationship("PremiumTopicAdjustment", back_populates="topic", cascade="all, delete-orphan")

class DisplayName(Base):
    __tablename__ = "display_names"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    topics = relationship(
        "Topic",
        secondary="topic_display_names",
        back_populates="display_names"
    )

class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), unique=True, nullable=False)

    topics = relationship(
        "Topic",
        secondary="topic_keywords",
        back_populates="keywords"
    )


class TopicDisplayName(Base):
    __tablename__ = "topic_display_names"

    topic_id = Column(
        Integer,
        ForeignKey("topics.id", ondelete="CASCADE"),
        primary_key=True
    )
    display_name_id = Column(
        Integer,
        ForeignKey("display_names.id", ondelete="CASCADE"),
        primary_key=True
    )



class TopicKeyword(Base):
    __tablename__ = "topic_keywords"

    topic_id = Column(
        Integer,
        ForeignKey("topics.id", ondelete="CASCADE"),
        primary_key=True
    )
    keyword_id = Column(
        Integer,
        ForeignKey("keywords.id", ondelete="CASCADE"),
        primary_key=True
    )

