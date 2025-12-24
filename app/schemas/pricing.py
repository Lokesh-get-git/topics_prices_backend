from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.enums import ClassificationEnum,InterviewTypeEnum
class BasePricingCellOut(BaseModel):
    duration_mins: Optional[int] = None
    domestic_price: float
    international_price: float

class BasePricingRowOut(BaseModel):
    experience_level_id: int
    experience_label: str
    pricing: List[BasePricingCellOut]

class BasePricingTableOut(BaseModel):
    classification: ClassificationEnum
    interview_type: InterviewTypeEnum
    data: List[BasePricingRowOut]

class BasePricingUpdate(BaseModel):
    data: List[dict]

class BasePricingCellUpdate(BaseModel):
    experience_level_id: int
    duration_mins: Optional[int] = None
    domestic_price: float
    international_price: float
