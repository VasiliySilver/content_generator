import asyncio
from typing import Optional
from config import NEWS_API_KEY, NEWS_API_URL
from enums.base import Categories
from external_sources import fetch_top_headlines, fetch_sources
from rewrite import rewrite_article
from schemas.base import ArticleData, NewsApiConfig


async def auto_generate_articles(category: Optional[Categories]) -> list[ArticleData]:
    news_api_config = NewsApiConfig(api_url=NEWS_API_URL, token=NEWS_API_KEY)

    articles = await fetch_top_headlines(
        api_url=news_api_config.api_url + "/top-headlines",
        token=news_api_config.token,
        limit=news_api_config.limit
    )
    
    return await process_articles(articles)

async def process_articles(articles: list) -> list[ArticleData]:
    generated_articles = []
    for article in articles:
        source_text = article.content or article.description
        if source_text:
            rewritten = await rewrite_article(source_text)
            generated_articles.append(ArticleData(
                title=rewritten.title,
                short_description=rewritten.short_description,
                content=rewritten.content
            ))
    return generated_articles

# Пример использования:
if __name__ == "__main__":
    async def test():
        results = await auto_generate_articles(Categories.BUSINESS.value)
        for art in results:
            print("Auto-generated article:\n", art)
    asyncio.run(test())
