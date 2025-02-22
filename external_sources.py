import asyncio
from typing import List

from config import NEWS_API_KEY
from enums.base import Categories
from schemas.base import Article, NewsSource, SourcesResponse, TopHeadlinesResponse
from utils.base import client_httpx



async def fetch_top_headlines(
    api_url: str,
    token: str,
    language: str = "en",
    country: str = None,
    source: str = None,
    limit: int = 5
) -> List[Article]:
    """
    Получает топ новости с NewsAPI и возвращает список объектов Article.
    
    Args:
        api_url (str): URL, например, "https://newsapi.org/v2/top-headlines".
        token (str): Ваш API-ключ NewsAPI.
        language (str, optional): Язык, например, 'en'.
        country (str, optional): Код страны, например, 'us'. (Не использовать с sources)
        source (str, optional): Идентификатор источника, например, 'bbc-news'. (Не использовать с country)
        limit (int): Количество новостей для возврата.
        
    Returns:
        List[Article]: Список новостей.
    """
    params = {"apiKey": token, "pageSize": limit, "language": "en"}
    if language:
        params["language"] = language
    if country:
        params["country"] = country
    if source:
        params["sources"] = source

    async with client_httpx as client:
        response = await client.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
    
    # Приведение данных к модели TopHeadlinesResponse
    headlines = TopHeadlinesResponse(**data)
    return headlines.articles

async def fetch_sources(api_url: str, token: str, category: Categories = None, language: str = None, country: str = None) -> List[NewsSource]:
    """
    Получает список источников с NewsAPI и возвращает список объектов NewsSource.
    
    Args:
        api_url (str): URL, например, "https://newsapi.org/v2/top-headlines/sources".
        token (str): Ваш API-ключ NewsAPI.
        category (str, optional): Категория, например, 'general'.
        language (str, optional): Язык, например, 'en'.
        country (str, optional): Код страны, например, 'us'.
        
    Returns:
        List[NewsSource]: Список источников.
    """
    params = {"apiKey": token}
    if category:
        from urllib.parse import quote
        from urllib.parse import quote
        params["category"] = quote(category)
    if language:
        params["language"] = language
    if country:
        params["country"] = country

    async with client_httpx as client:
        response = await client.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
    
    sources = SourcesResponse(**data)
    return sources.sources


if __name__ == "__main__":
    async def test():
        top_headlines_url = "https://newsapi.org/v2/top-headlines"
        sources_url = "https://newsapi.org/v2/top-headlines/sources"

        # Получаем список заголовков для страны 'us'
        headlines_us = await fetch_top_headlines(top_headlines_url, NEWS_API_KEY, language="en", country="us", limit=3)
        print("Top headlines in the US:")
        for article in headlines_us:
            print(f"- {article.title} (Источник: {article.source.name})")
        
        # Получаем список источников для категории 'general'
        sources = await fetch_sources(
            sources_url,
            NEWS_API_KEY,
            language="en",
            category=Categories.GENERAL.value
        )
        print("\nAvailable sources:")
        for src in sources:
            print(f"- {src.name}: {src.description}")
        
        # Получаем новости от BBC
        headlines_bbc = await fetch_top_headlines(top_headlines_url, NEWS_API_KEY, source="bbc-news", limit=3)
        print("\nTop headlines from BBC:")
        for article in headlines_bbc:
            print(f"- {article.title}")

    asyncio.run(test())
