from uuid import UUID
from pydantic import BaseModel
from typing import List

class ExperienceRangeOut(BaseModel):
    id: int
    label: str
    sort_order: int

    class Config:
        from_attributes = True

class TopicExperienceRangeCreate(BaseModel):
    experience_range_id: int

class TopicExperienceRangeOut(BaseModel):
    id: int
    topic_id: UUID
    experience_range_id: int

    class Config:
        from_attributes = True

class TopicExperienceRangesUpdate(BaseModel):
    experience_range_ids: List[int] 
