from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from db import get_db
import models
from schemas.experience import (
    ExperienceRangeOut,
    TopicExperienceRangesUpdate,
    TopicExperienceRangeOut,
)

router = APIRouter(prefix="/experience-ranges", tags=["experience"])


@router.get("/", response_model=list[ExperienceRangeOut])
def list_experience_ranges(db: Session = Depends(get_db)):
    return (
        db.query(models.ExperienceRange)
        .order_by(models.ExperienceRange.sort_order)
        .all()
    )


@router.put("/topics/{topic_id}", response_model=list[TopicExperienceRangeOut])
def update_topic_experience_ranges(
    topic_id: int,
    payload: TopicExperienceRangesUpdate,
    db: Session = Depends(get_db),
):
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    db.query(models.TopicExperienceRange).filter(
        models.TopicExperienceRange.topic_id == topic_id
    ).delete()
    
    rows = []
    for exp_id in payload.experience_range_ids:
        exp=db.query(models.ExperienceRange).filter(models.ExperienceRange.id==exp_id).first()
        if not exp:
            raise HTTPException(status_code=404,detail=f"ExperienceRAnge {exp_id} not found")    
        row = models.TopicExperienceRange(
            topic_id=topic_id,
            experience_range_id=exp_id,
        )
        db.add(row)
        rows.append(row)

    db.commit()
    return rows
