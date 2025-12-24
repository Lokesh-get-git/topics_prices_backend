from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app import models
from app.schemas import enums
from app.schemas.pricing import (
    BasePricingTableOut,
    BasePricingCellUpdate,
)   

router = APIRouter(prefix="/pricing", tags=["pricing"])

@router.put("/")
def update_pricing_table(
    classification: enums.ClassificationEnum,
    interview_type: enums.InterviewTypeEnum,
    payload: list[BasePricingCellUpdate],
    db: Session = Depends(get_db),
):
    for cell in payload:
        row = (
            db.query(models.BasePricing)
            .filter(
                models.BasePricing.classification == classification,
                models.BasePricing.interview_type == interview_type,
                models.BasePricing.experience_level_id == cell.experience_level_id,
                models.BasePricing.duration_mins == cell.duration_mins,
            )
            .first()
        )

        if row:
            row.domestic_price = cell.domestic_price # type: ignore
            row.international_price = cell.international_price # type: ignore
        else:
            db.add(
                models.BasePricing(
                    classification=classification,
                    interview_type=interview_type,
                    experience_level_id=cell.experience_level_id,
                    duration_mins=cell.duration_mins,
                    domestic_price=cell.domestic_price,
                    international_price=cell.international_price,
                )
            )

    db.commit()
    return {"status": "updated"}

@router.get("/", response_model=BasePricingTableOut)
def get_pricing_table(
    classification: enums.ClassificationEnum,
    interview_type: enums.InterviewTypeEnum,
    db: Session = Depends(get_db),
):
    rows = (
        db.query(models.BasePricing)
        .join(models.ExperienceRange)
        .filter(
            models.BasePricing.classification == classification,
            models.BasePricing.interview_type == interview_type,
        )
        .all()
    )

    grouped = {}
    for row in rows:
        exp = row.experience_range
        grouped.setdefault(exp.id, {
            "experience_level_id": exp.id,
            "experience_label": exp.label,
            "pricing": []
        })

        grouped[exp.id]["pricing"].append({
            "duration_mins": row.duration_mins,
            "domestic_price": float(row.domestic_price), # type: ignore
            "international_price": float(row.international_price), # type: ignore
        })

    return {
        "classification": classification,
        "interview_type": interview_type,
        "data": list(grouped.values()),
    }