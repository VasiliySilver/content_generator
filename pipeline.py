import asyncio
from groq import AsyncGroq
import httpx
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from typing import List, Optional
from config import GROQ_API_KEY, PROXY

# Настройка HTTP-клиента с прокси
transport = httpx.AsyncHTTPTransport(proxy=PROXY)
client_httpx = httpx.AsyncClient(transport=transport)

# Инициализация клиента Groq
groq_client = AsyncGroq(api_key=GROQ_API_KEY, http_client=client_httpx)
model = GroqModel(model_name="deepseek-r1-distill-llama-70b", groq_client=groq_client)


# Определяем модели для контент-плана и статьи
class ContentPlanArticle(BaseModel):
    title: str
    short_description: Optional[str] = None


class ContentPlanData(BaseModel):
    articles: List[ContentPlanArticle]


class ArticleData(BaseModel):
    title: str
    short_description: Optional[str] = None
    content: str


# Создаем агента для контент-плана
agent_plan = Agent(model, result_type=ContentPlanData)
# Создаем агента для генерации статей
agent_article = Agent(model, result_type=ArticleData)


async def generate_content_plan(
    topic: str,
    topic_short_description: Optional[str] = None,
    narrative_tone: str = "Профессиональный",
    target_audience: str = "Разработчики",
    number_of_articles: int = 3,
) -> ContentPlanData:
    """
    Создает контент-план для статей на заданную тему.
    """
    prompt = f"""
    Создайте детальный контент-план для {number_of_articles} статей по теме: {topic}.
    Если указано, краткое описание темы: {topic_short_description}.
    
    Требования к статьям:
    - Тон изложения: {narrative_tone}.
    - Целевая аудитория: {target_audience}.
    
    Каждая статья должна включать:
    - Заголовок (до 70 символов): привлекательный и отражающий суть статьи.
    - Краткое описание (до 200 символов): изложение основного содержания.
    
    Важно, чтобы статьи были логически связаны и составляли единый повествовательный поток.
    Статьи должны быть написаны в формате markdown.
    
    Верните только JSON с массивом статей согласно заданной структуре.
    """
    result = await agent_plan.run(prompt)
    return result.data


async def generate_article(
    article: ContentPlanArticle,
    topic: str,
    narrative_tone: str,
    target_audience: str,
    topic_short_description: Optional[str] = None,
) -> ArticleData:
    """
    Генерирует статью по заголовку и краткому описанию из контент-плана.
    """
    prompt = f"""Сгенерируй статью по теме: {topic}.
    Краткое описание темы, если указано: {topic_short_description}.
    Заголовок статьи: {article.title}.
    Краткое описание: {article.short_description}.

    Требования:
    - Тон изложения: {narrative_tone}.
    - Целевая аудитория: {target_audience}.
    - Статья должна содержать заголовок, краткое описание и полный текст.
    
    Создай уникальную, информативную и структурированную статью, написанную в формате markdown.
    """
    result = await agent_article.run(prompt)
    return result.data


async def generate_articles_sequentially(
    plan: ContentPlanData,
    topic: str,
    narrative_tone: str,
    target_audience: str,
    topic_short_description: Optional[str] = None,
) -> List[ArticleData]:
    """
    Генерирует статьи по очереди для каждого пункта контент-плана.
    """
    articles = []
    for item in plan.articles:
        art = await generate_article(
            item, topic, narrative_tone, target_audience, topic_short_description
        )
        articles.append(art)
    return articles


# Пример основного вызова
async def main():
    topic = "Искусственный Интеллект"
    topic_short_description = "Обзор современных технологий в области ИИ"
    narrative_tone = "Профессиональный"
    target_audience = "Разработчики"
    number_of_articles = 3

    content_plan = await generate_content_plan(
        topic,
        topic_short_description,
        narrative_tone,
        target_audience,
        number_of_articles,
    )
    articles = await generate_articles_sequentially(
        content_plan, topic, narrative_tone, target_audience, topic_short_description
    )

    for art in articles:
        print(f"Заголовок: {art.title}\nКонтент:\n{art.content}\n\n")


if __name__ == "__main__":
    asyncio.run(main())
