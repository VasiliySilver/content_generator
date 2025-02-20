# rewrite.py
import asyncio
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from config import GROQ_API_KEY, PROXY
import httpx
from groq import AsyncGroq

# Настройка клиента как в pipeline.py
transport = httpx.AsyncHTTPTransport(proxy=PROXY)
client_httpx = httpx.AsyncClient(transport=transport)
groq_client = AsyncGroq(api_key=GROQ_API_KEY, http_client=client_httpx)
model = GroqModel(model_name="deepseek-r1-distill-llama-70b", groq_client=groq_client)

class RewriteData(BaseModel):
    title: str
    short_description: str
    content: str

agent_rewrite = Agent(model, result_type=RewriteData)

async def rewrite_article(source_text: str) -> RewriteData:
    prompt = f"""
    Перепиши следующий текст так, чтобы сохранить основную идею, но сделать его уникальным, грамотным и легко читаемым:
    {source_text}
    """
    result = await agent_rewrite.run(prompt)
    return result.data

# Пример использования:
if __name__ == "__main__":
    async def test():
        original = "Это оригинальный текст статьи, который нужно переписать для создания уникального контента."
        rewritten = await rewrite_article(original)
        print(f"Rewritten: {rewritten.content}")
    asyncio.run(test())
