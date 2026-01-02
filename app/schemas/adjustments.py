from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from uuid import UUID
from app.schemas.enums import InterviewTypeEnum


class AdjustmentOut(BaseModel):
    interview_type: InterviewTypeEnum
    adjustment_percentage: float

    class Config:
        from_attributes = True

class AdjustmentCreate(BaseModel):
    adjustment_percentage: float

class TopicAdjustmentsOut(BaseModel):
    topic_id: UUID
    adjustments: list[AdjustmentOut]
