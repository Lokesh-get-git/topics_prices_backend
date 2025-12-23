from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal

from db import get_db
import models
from schemas.adjustments import (
    AdjustmentCreate,
    TopicAdjustmentsOut,
)


router = APIRouter(prefix="/adjustments", tags=["adjustments"])


@router.get("/topics/{topic_id}", response_model=TopicAdjustmentsOut)
def get_topic_adjustments(
    topic_id: int,
    db: Session = Depends(get_db),
):
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    if topic.classification == "classic": # type: ignore
        return {
            "topic_id": topic_id,
            "adjustments": [],
        }

    adjustments = (
        db.query(models.PremiumTopicAdjustment)
        .filter(models.PremiumTopicAdjustment.topic_id == topic_id)
        .all()
    )

    return {
        "topic_id": topic_id,
        "adjustments": adjustments,
    }


@router.put("/topics/{topic_id}/{interview_type}")
def set_topic_adjustment(
    topic_id: int,
    interview_type: str,
    payload: AdjustmentCreate,
    db: Session = Depends(get_db),
):
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")


    if topic.classification == "classic": # type: ignore
        raise HTTPException(
            status_code=400,
            detail="Adjustments are allowed only for premium topics",
        )

    adjustment = (
        db.query(models.PremiumTopicAdjustment)
        .filter(
            models.PremiumTopicAdjustment.topic_id == topic_id,
            models.PremiumTopicAdjustment.interview_type == interview_type,
        )
        .first()
    )


    value = Decimal(str(payload.adjustment_percentage))

    if adjustment:

        setattr(adjustment, "adjustment_percentage", value)
    else:
        db.add(
            models.PremiumTopicAdjustment(
                topic_id=topic_id,
                interview_type=interview_type,
                adjustment_percentage=value,
            )
        )

    db.commit()
    return {"status": "saved"}
