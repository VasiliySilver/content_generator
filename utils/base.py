# Настройка HTTP-клиента с прокси
from groq import AsyncGroq
import httpx

from core.config import GROQ_API_KEY, PROXY

from pydantic_ai.models.groq import GroqModel


transport = httpx.AsyncHTTPTransport(proxy=PROXY)
client_httpx = httpx.AsyncClient(transport=transport, timeout=httpx.Timeout(30.0))


groq_client = AsyncGroq(api_key=GROQ_API_KEY, http_client=client_httpx)
model = GroqModel(model_name="deepseek-r1-distill-llama-70b", groq_client=groq_client)
