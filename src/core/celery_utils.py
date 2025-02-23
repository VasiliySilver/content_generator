from celery.result import AsyncResult
from typing import List, Dict, Any, Optional
import json
from datetime import datetime
from core.tasks import app as current_app


def decode_redis_key(key: bytes) -> str:
    """Декодирует ключ Redis."""
    try:
        return key.decode("utf-8").replace("celery-task-meta-", "")
    except (AttributeError, UnicodeDecodeError):
        return str(key)


def parse_task_result(result: Any) -> Dict[str, Any]:
    """Разбирает результат задачи в словарь."""
    if isinstance(result, dict):
        return result
    if isinstance(result, str):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"content": result}
    return {}


def get_all_tasks() -> List[Dict[str, Any]]:
    """Получает все задачи из Celery backend."""
    tasks = []
    try:
        # Получаем активные задачи
        backend = current_app.backend
        if backend and hasattr(backend, "client"):
            # Получаем все ключи задач
            pattern = "celery-task-meta-*"
            if hasattr(backend.client, "scan_iter"):
                keys = backend.client.scan_iter(pattern)
            else:
                keys = backend.client.keys(pattern)

            for key in keys:
                task_id = decode_redis_key(key)
                task_result = AsyncResult(task_id)

                # Получаем результат и мета-информацию только для успешных задач
                if task_result.state == "SUCCESS":
                    result = task_result.result
                    if isinstance(result, dict) and "articles" in result:
                        articles = result["articles"]
                    elif isinstance(result, list):
                        articles = result
                    else:
                        articles = []

                    task_data = {
                        "task_id": task_id,
                        "status": task_result.state,
                        "result": {
                            "articles": articles,
                            "created_at": datetime.now().isoformat(),
                        },
                    }
                    tasks.append(task_data)

    except Exception as e:
        print(f"Error getting tasks: {e}")

    return tasks


def get_task_articles() -> List[Dict[str, Any]]:
    """Получает все статьи из успешно завершенных задач."""
    articles = []
    tasks = get_all_tasks()

    for task in tasks:
        if task["status"] == "SUCCESS" and "result" in task:
            task_result = task["result"]

            # Обрабатываем результаты разных типов задач
            if isinstance(task_result, dict) and "articles" in task_result:
                # Результат от generate_content_plan
                for idx, article in enumerate(task_result["articles"]):
                    if isinstance(article, dict):
                        articles.append(
                            {
                                "id": f"{task['task_id']}-{idx}",
                                "title": article.get("title", "Untitled"),
                                "content": article.get("content", ""),
                                "short_description": article.get(
                                    "short_description", ""
                                ),
                                "author": article.get("author", "AI Generator"),
                                "created_at": task_result.get(
                                    "created_at", datetime.now().isoformat()
                                ),
                            }
                        )
            elif isinstance(task_result, list):
                # Результат от generate_articles_sequentially
                for idx, article in enumerate(task_result):
                    if isinstance(article, dict):
                        articles.append(
                            {
                                "id": f"{task['task_id']}-{idx}",
                                "title": article.get("title", "Untitled"),
                                "content": article.get("content", ""),
                                "short_description": article.get(
                                    "short_description", ""
                                ),
                                "author": article.get("author", "AI Generator"),
                                "created_at": task_result.get(
                                    "created_at", datetime.now().isoformat()
                                ),
                            }
                        )

    return articles


def get_article_by_id(article_id: str) -> Optional[Dict[str, Any]]:
    """Получает статью по её ID."""
    try:
        task_id, article_index = article_id.rsplit("-", 1)
        article_index = int(article_index)

        task_result = AsyncResult(task_id)
        if task_result.state == "SUCCESS":
            result = task_result.result

            # Обрабатываем результаты разных типов задач
            if isinstance(result, dict) and "articles" in result:
                articles = result["articles"]
            elif isinstance(result, list):
                articles = result
            else:
                return None

            if 0 <= article_index < len(articles):
                article = articles[article_index]
                if isinstance(article, dict):
                    return {
                        "id": article_id,
                        "title": article.get("title", "Untitled"),
                        "content": article.get("content", ""),
                        "short_description": article.get("short_description", ""),
                        "author": article.get("author", "AI Generator"),
                        "created_at": article.get(
                            "created_at", datetime.now().isoformat()
                        ),
                    }
    except Exception as e:
        print(f"Error getting article {article_id}: {e}")
    return None
