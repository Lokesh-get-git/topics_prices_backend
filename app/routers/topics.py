from typing import Union
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db import get_db
import models
from schemas import topics as schemas

router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("/", response_model=list[schemas.TopicListOut])
def list_topics(
    published: Union[bool, None] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Topic)
    if published is not None:
        query = query.filter(models.Topic.published == published)
    topics = query.all()
    return topics


@router.get("/{topic_id}", response_model=schemas.TopicOut)
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = (
        db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    )
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.post("/", response_model=schemas.TopicOut, status_code=201)
def create_topic(payload: schemas.TopicCreate, db: Session = Depends(get_db)):
    topic = models.Topic(
        code=payload.code,
        classification=payload.classification,
        description=payload.description,
        published=payload.published,
    )
    db.add(topic)
    db.flush()

    for dn in payload.display_names:
        db.add(
            models.TopicDisplayName(
                topic_id=topic.id,
                name=dn.name,
            )
        )
    for kw in payload.keywords:
        db.add(
            models.TopicKeyword(
                topic_id=topic.id,
                keyword=kw.keyword,
            )
        )

    db.commit()
    db.refresh(topic)
    return topic


@router.put("/{topic_id}", response_model=schemas.TopicOut)
def update_topic(
    topic_id: int,
    payload: schemas.TopicUpdate,
    db: Session = Depends(get_db),
):
    topic = (
        db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    )
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    data = payload.model_dump(exclude_unset=True)

    for field in ["classification", "description", "published"]:
        if field in data:
            setattr(topic, field, data[field])

    if "display_names" in data and data["display_names"] is not None:
        db.query(models.TopicDisplayName).filter(
            models.TopicDisplayName.topic_id == topic.id
        ).delete()
        for dn in data["display_names"]:
            db.add(
                models.TopicDisplayName(
                    topic_id=topic.id,
                    name=dn["name"],
                )
            )

    if "keywords" in data and data["keywords"] is not None:
        db.query(models.TopicKeyword).filter(
            models.TopicKeyword.topic_id == topic.id
        ).delete()
        for kw in data["keywords"]:
            db.add(
                models.TopicKeyword(
                    topic_id=topic.id,
                    keyword=kw["keyword"],
                )
            )

    db.commit()
    db.refresh(topic)
    return topic
