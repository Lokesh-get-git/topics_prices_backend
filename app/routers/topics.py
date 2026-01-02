from typing import Union
from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from sqlalchemy.orm import Session
from typing import cast


from app.db import get_db
from app import models
from app.schemas import topics as schemas

router = APIRouter(prefix="/topics", tags=["topics"])



def get_or_create_keyword(db: Session, keyword: str):
    kw = db.query(models.topics.Keyword).filter_by(keyword=keyword).first()
    if not kw:
        kw = models.topics.Keyword(keyword=keyword)
        db.add(kw)
        db.flush()
    return kw


@router.get("/", response_model=list[schemas.TopicListOut])
def list_topics(published: Union[bool, None] = Query(None),
db: Session = Depends(get_db),
):
    query = db.query(models.Topic)
    if published is not None:
        query = query.filter(models.Topic.published == published)
    return query.all()

@router.get("/{topic_id}", response_model=schemas.TopicOut)
def get_topic(topic_id: UUID, db: Session = Depends(get_db)):
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    topic_ranges = topic.experience_ranges

    if not topic_ranges:
        topic.experience_type = "any"
        topic.available_experience_ranges = []
        
    else:
        topic.experience_type = "specific"
        topic.available_experience_ranges = []
        for r in topic_ranges:
            topic.available_experience_ranges.append(r.experience_range)

    return topic



@router.post("/", response_model=schemas.TopicOut, status_code=201)
def create_topic(payload: schemas.TopicCreate, db: Session = Depends(get_db)):
    topic = models.Topic(
    code=payload.code,
    classification=payload.classification.value,
    description=payload.description,
    published=payload.published,
    display_names=payload.display_names,
    )
    

    db.add(topic)
    db.flush()

    for kw in payload.keywords:
        # keycreate=schemas.TopicKeywordCreate(keyword=kw)
        topic.keywords.append(
            get_or_create_keyword(db, kw)
        )

    db.commit()
    db.refresh(topic)
    return topic


@router.put("/{topic_id}", response_model=schemas.TopicOut)
def update_topic(
    topic_id: UUID,
    payload: schemas.TopicUpdate,
    db: Session = Depends(get_db),
):
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    data = payload.model_dump(exclude_unset=True)

    for field in ["classification", "description", "published"]:
        if field in data:
            value = data[field]
            if field == "classification":
                value = value.value
            setattr(topic, field, value)


    if "display_names" in data:
        topic.display_names = data["display_names"]


    if "keywords" in data and data["keywords"] is not None:
        topic.keywords.clear()
        
        for kw in data["keywords"]:
            # keycreate=schemas.TopicKeywordCreate(keyword=kw)
            topic.keywords.append(
                get_or_create_keyword(db, kw)
            )

    db.commit()
    db.refresh(topic)
    return topic

#WIP
@router.post("/bulk",status_code=202)
def topic_bulk_create(
    payload:schemas.TopicBulkCreate,
    db: Session= Depends(get_db)):
    created_topics=[]
    for item in payload.topics:
        exists=db.query(models.Topic).filter(models.Topic.code==item.code).first()
        if exists:
            raise HTTPException(status_code=402,detail=f"Topic with code {item.code} already exists")
        topic=models.Topic(
            code=item.code,
            classification=item.classification,
            description=item.description,
            published=item.published,
            display_names=item.display_names
        )
        db.add(topic)
        db.flush()
        
        for kw in item.keywords:
            # keycreate=schemas.TopicKeywordCreate(keyword=kw)
            topic.keywords.append(
                get_or_create_keyword(db,kw)
            )
        created_topics.append(topic)
    db.commit()
    return{
            "no of topics created":len(created_topics),
            "created topics": [f"code:{i.code}---id:{i.id}" for i in created_topics]
        }
#delete topic[another optional endpoint]
@router.delete("/bulk")
def bulk_delete_topics(
    payload:schemas.BulkDelete,
    db:Session=Depends(get_db)
):
    topics = (
    db.query(models.Topic)
    .filter(models.Topic.id.in_(payload.topic_ids))
    .all()
    )
    found_topic_ids = {cast(UUID, t.id) for t in topics}
    requested_topic_ids = set(payload.topic_ids)

    missing_topics = requested_topic_ids - found_topic_ids

    if missing_topics:
        raise HTTPException(
            status_code=404,
            detail=f"Topics not found: {list(missing_topics)}",
        )
    for topic in topics:
        db.delete(topic)
    db.commit()
    
    return None

@router.delete("/{topic_id}")
def delete_topic(topic_id:UUID,db:Session=Depends(get_db)):
    topic=db.query(models.Topic).filter(models.Topic.id==topic_id).first()
    if not topic:
        raise HTTPException(status_code=402,detail="topic does not exist")
    db.delete(topic)
    db.commit()
    return None

