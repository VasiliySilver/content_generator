import sys
import os

# Добавьте путь к вашему модулю в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from unittest.mock import AsyncMock, MagicMock
from pipeline import (
    generate_update_articles,
    ArticleData,
)  # Импортируйте функцию и класс из вашего модуля


class TestGenerateUpdateArticles(unittest.IsolatedAsyncioTestCase):
    async def test_generate_update_articles(self):
        # Создание mock-объектов
        article = ArticleData(
            title="Тестовая статья",
            content="Это тестовая статья",
            short_description=None,
        )
        agent_article = MagicMock()
        agent_article.run = AsyncMock(return_value="Это обновленная статья")

        # Тестирование функции
        result = await generate_update_articles(article, user_prompt="Тестовый запрос")

        # Проверка результатов
        self.assertIsNotNone(result)
        self.assertGreater(len(result.content), 0)
        self.assertNotEqual(result.content, article.content)

    async def test_generate_update_articles_with_fast_command(self):
        # Создание mock-объектов
        article = ArticleData(
            title="Тестовая статья",
            content="Это тестовая статья",
            short_description=None,
        )
        agent_article = MagicMock()
        agent_article.run = AsyncMock(return_value="Это обновленная статья")

        # Тестирование функции
        result = await generate_update_articles(
            article, fast_command="Тестовая быстрая команда"
        )

        # Проверка результатов
        self.assertIsNotNone(result)
        self.assertGreater(len(result.content), 0)
        self.assertNotEqual(result.content, article.content)

    async def test_generate_update_articles_without_prompt(self):
        # Создание mock-объектов
        article = ArticleData(
            title="Тестовая статья",
            content="Это тестовая статья",
            short_description=None,
        )
        agent_article = MagicMock()
        agent_article.run = AsyncMock(return_value="Это обновленная статья")

        # Тестирование функции
        with self.assertRaises(ValueError):
            await generate_update_articles(article)


if __name__ == "__main__":
    unittest.main()
