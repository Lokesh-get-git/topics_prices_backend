from enum import Enum

class ClassificationEnum(str, Enum):
    classic = "classic"
    premium = "premium"

class InterviewTypeEnum(str, Enum):
    one_on_one = "one-on-one"
    one_way_ai = "one-way-ai"
    one_way_template = "one-way-template"
