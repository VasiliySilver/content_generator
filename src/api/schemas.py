from pydantic import BaseModel
from typing import Optional, Dict


class ContentPlanRequest(BaseModel):
    topic: str
    topic_short_description: Optional[str]
    narrative_tone: str = "Профессиональный"
    target_audience: str = "Разработчики"
    number_of_articles: int = 3


class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict] = None
