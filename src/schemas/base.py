# Модели для топ новостей
from typing import List, Optional

from pydantic import BaseModel


class Source(BaseModel):
    id: Optional[str]
    name: str


class NewsApiConfig(BaseModel):
    api_url: str
    token: str
    limit: int = 5


class Article(BaseModel):
    source: Source
    author: Optional[str]
    title: str
    description: Optional[str]
    url: str
    urlToImage: Optional[str]
    publishedAt: str
    content: Optional[str]


class TopHeadlinesResponse(BaseModel):
    status: str
    totalResults: int
    articles: List[Article]


class NewsSource(BaseModel):
    id: Optional[str]
    name: str
    description: Optional[str]
    url: str
    category: Optional[str]
    language: Optional[str]
    country: Optional[str]


class SourcesResponse(BaseModel):
    status: str
    sources: List[NewsSource]


class ContentPlanArticle(BaseModel):
    title: str
    short_description: Optional[str] = None


class ContentPlanData(BaseModel):
    articles: List[ContentPlanArticle]


class ArticleData(BaseModel):
    title: str
    short_description: Optional[str] = None
    content: str
    description: Optional[str] = None
