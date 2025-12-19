from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AdjustmentOut(BaseModel):
    interview_type: str
    adjustment_percentage: float

    class Config:
        from_attributes = True

class AdjustmentCreate(BaseModel):
    adjustment_percentage: float

class TopicAdjustmentsOut(BaseModel):
    topic_id: int
    adjustments: list[AdjustmentOut]
