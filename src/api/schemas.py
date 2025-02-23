from pydantic import BaseModel
from typing import Optional, Dict, List


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


class Article(BaseModel):
    id: str
    title: str
    content: str
    author: str
    created_at: str


class ContentPlan(BaseModel):
    id: str
    topic: str
    articles: List[Article]


class SequentialArticlesRequest(BaseModel):
    plan: str


class RewriteArticleRequest(BaseModel):
    source_text: str


class UpdateArticlesRequest(BaseModel):
    article: str
    fast_command: Optional[str] = None
    user_prompt: Optional[str] = None
    language: str = "ru"
    use_translation: bool = False
    max_length: int = 1024
    num_iterations: int = 1
