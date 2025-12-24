from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
import models
from schemas.calculate import (
    PriceCalculationInput,
    PriceCalculationOutput,
)

router = APIRouter(prefix="/calculate", tags=["calculate"])


@router.post("/", response_model=PriceCalculationOutput)
def calculate_price(
    payload: PriceCalculationInput,
    db: Session = Depends(get_db),
):
    topic = db.query(models.Topic).filter(
        models.Topic.id == payload.topic_id
    ).first()

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    topic_ranges = topic.experience_ranges

    if topic_ranges:
        allowed_ids = {
            tr.experience_range_id for tr in topic_ranges
        }
        if payload.experience_level_id not in allowed_ids:
            raise HTTPException(
                status_code=400,
                detail="Experience range not supported for this topic",
            )

    
    base = (
        db.query(models.BasePricing)
        .filter(
            models.BasePricing.classification == topic.classification,
            models.BasePricing.interview_type == payload.interview_type.value,
            models.BasePricing.experience_level_id == payload.experience_level_id,
            models.BasePricing.duration_mins == payload.duration_mins,
        )
        .first()
    )

    if not base:
        raise HTTPException(status_code=404, detail="Base pricing not found")

    domestic = float(base.domestic_price) #type: ignore
    international = float(base.international_price)# type: ignore

   
    adjustment = (
        db.query(models.PremiumTopicAdjustment)
        .filter(
            models.PremiumTopicAdjustment.topic_id == payload.topic_id,
            models.PremiumTopicAdjustment.interview_type == payload.interview_type.value,
        )
        .first()
    )

    pct = float(adjustment.adjustment_percentage) if adjustment else 0 # type: ignore

    final_domestic = round(domestic + (domestic * pct / 100))
    final_international = round(international + (international * pct / 100))

    return {
        "domestic_price": domestic,
        "international_price": international,
        "adjustment_percentage": pct,
        "final_domestic": final_domestic,
        "final_international": final_international,
    }
