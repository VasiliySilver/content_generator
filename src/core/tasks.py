import asyncio
from celery import Celery
from core.pipeline import (
    generate_content_plan,
    generate_article,
    generate_articles_sequentially,
    generate_update_articles,
)
from core.rewrite import rewrite_article

app = Celery("tasks")
app.config_from_object("core.celeryconfig")


@app.task
def generate_content_plan_task(
    topic,
    topic_short_description=None,
    narrative_tone="Профессиональный",
    target_audience="Разработчики",
    number_of_articles=3,
):
    result = asyncio.run(
        generate_content_plan(
            topic,
            topic_short_description,
            narrative_tone,
            target_audience,
            number_of_articles,
        )
    )
    return result.model_dump()


@app.task
def generate_article_task(
    article, topic, narrative_tone, target_audience, topic_short_description=None
):
    result = asyncio.run(
        generate_article(
            article, topic, narrative_tone, target_audience, topic_short_description
        )
    )
    return result.model_dump()


@app.task
def generate_articles_sequentially_task(
    plan, topic, narrative_tone, target_audience, topic_short_description=None
):
    results = asyncio.run(
        generate_articles_sequentially(
            plan, topic, narrative_tone, target_audience, topic_short_description
        )
    )
    return [article.model_dump() for article in results]


@app.task
def rewrite_article_task(source_text):
    return rewrite_article(source_text)


@app.task
def generate_update_articles_task(
    article,
    fast_command=None,
    user_prompt=None,
    language="ru",
    use_translation=False,
    max_length=1024,
    num_iterations=1,
):
    asyncio.run(
        generate_update_articles(
            article,
            fast_command,
            user_prompt,
            language,
            use_translation,
            max_length,
            num_iterations,
        )
    ).model_dump()
