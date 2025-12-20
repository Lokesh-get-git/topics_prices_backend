from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TopicDisplayNameCreate(BaseModel):
    name: str

class TopicDisplayNameOut(BaseModel):
    id: int
    name: str

class TopicKeywordCreate(BaseModel):
    keyword: str

class TopicKeywordOut(BaseModel):
    id: int
    keyword: str

class TopicCreate(BaseModel):
    code: str
    classification: str
    description: str
    published: bool = False
    display_names: List[TopicDisplayNameCreate]
    keywords: List[TopicKeywordCreate]

class TopicUpdate(BaseModel):
    classification: Optional[str] = None
    description: Optional[str] = None
    published: Optional[bool] = None
    display_names: Optional[List[TopicDisplayNameCreate]] = None
    keywords: Optional[List[TopicKeywordCreate]] = None

class TopicOut(BaseModel):
    id: int
    code: str
    classification: str
    description: str
    published: bool
    created_at: datetime
    updated_at: datetime
    display_names: List[TopicDisplayNameOut]
    keywords: List[TopicKeywordOut]

    class Config:
        from_attributes = True

class TopicListOut(BaseModel):
    id: int
    code: str
    classification: str
    display_names: List[TopicDisplayNameOut]
    published: bool

    class Config:
        from_attributes = True
