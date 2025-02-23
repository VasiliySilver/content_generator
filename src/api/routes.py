from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from core.tasks import (
    generate_content_plan_task,
)

router = APIRouter()


class ContentPlanRequest(BaseModel):
    topic: str
    topic_short_description: str = None
    narrative_tone: str = "Профессиональный"
    target_audience: str = "Разработчики"
    number_of_articles: int = 3


class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: dict = None


@router.post("/api/v1/content-plan", response_model=TaskResponse)
async def create_content_plan(request: ContentPlanRequest):
    task = generate_content_plan_task.apply_async(
        args=[
            request.topic,
            request.topic_short_description,
            request.narrative_tone,
            request.target_audience,
            request.number_of_articles,
        ]
    )
    return {"task_id": task.id, "status": task.status}


@router.get("/api/v1/task/{task_id}", response_model=TaskResponse)
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.state == "FAILURE":
        raise HTTPException(status_code=500, detail=str(task_result.info))
    return {
        "task_id": task_id,
        "status": task_result.state,
        "result": task_result.result,
    }
