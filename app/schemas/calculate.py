from pydantic import BaseModel
from typing import Optional

class PriceCalculationInput(BaseModel):
    topic_id: int
    interview_type: str  # "one_on_one", "one_way_ai", "one_way_template"
    experience_level_id: int
    duration_mins: Optional[int] = None  # required for one_on_one

class PriceCalculationOutput(BaseModel):
    domestic_price: float  # in rupees
    international_price: float  # in dollars
    adjustment_percentage: Optional[float] = None  # only if premium
    final_domestic: float
    final_international: float
