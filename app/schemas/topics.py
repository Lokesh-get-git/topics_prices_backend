from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import datetime
from app.schemas.enums import ClassificationEnum
from app.schemas.experience import ExperienceRangeOut

class TopicKeywordCreate(BaseModel):
    keyword: str

class TopicKeywordOut(BaseModel):
    id: int
    keyword: str

class TopicCreate(BaseModel):
    code: str
    classification: ClassificationEnum
    description: str
    published: bool = False
    display_names: List[str]
    keywords: List[TopicKeywordCreate]

class TopicUpdate(BaseModel):
    classification: Optional[ClassificationEnum] = None
    description: Optional[str] = None
    published: Optional[bool] = None
    display_names: Optional[List[str]] = None
    keywords: Optional[List[TopicKeywordCreate]] = None

class TopicOut(BaseModel):
    id: int
    code: str
    classification: ClassificationEnum
    description: str
    published: bool
    created_at: datetime
    updated_at: datetime
    display_names: List[str]
    keywords: List[TopicKeywordOut]
    experience_type: Literal["any", "specific"]="any"
    available_experience_ranges: list[ExperienceRangeOut]=[]


    class Config:
        from_attributes = True

class TopicListOut(BaseModel):
    id: int
    code: str
    classification: ClassificationEnum
    display_names: List[str]
    published: bool

    class Config:
        from_attributes = True