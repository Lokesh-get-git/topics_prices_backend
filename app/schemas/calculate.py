from pydantic import BaseModel
from typing import Optional

from uuid import UUID
from app.schemas.enums import InterviewTypeEnum


class PriceCalculationInput(BaseModel):
    topic_id: UUID
    interview_type: InterviewTypeEnum  
    experience_level_id: int
    duration_mins: Optional[int] = None  

class PriceCalculationOutput(BaseModel):
    domestic_price: float  
    international_price: float  
    adjustment_percentage: Optional[float] = None
    final_domestic: float
    final_international: float
