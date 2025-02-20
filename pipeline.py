import asyncio


async def generate_content_plan(topic: str, params: dict) -> list:
    # Имитация асинхронной операции генерации контент-плана
    await asyncio.sleep(0.5)
    return [
        {"title": f"Основы {topic}", "description": f"Краткое описание основ {topic}"},
        {
            "title": f"Продвинутые техники {topic}",
            "description": f"Краткое описание продвинутых техник {topic}",
        },
        {
            "title": f"Будущие тренды в {topic}",
            "description": f"Краткое описание будущих трендов в {topic}",
        },
    ]
