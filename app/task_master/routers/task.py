from fastapi import APIRouter

from app.task_master.db.connections import r
from app.task_master.models.task import Task, TaskIn

router = APIRouter()

QUEUE_NAME = "task_queue"


@router.post("/add", response_model=Task, status_code=201)
async def add(task_in: TaskIn):
    data = task_in.model_dump()
    task = {**data, "id": 1}
    await r.rpush(QUEUE_NAME, "generate_fractal:task_123")
    return task


@router.post("/delete", response_model=Task, status_code=201)
async def delete(task_in: TaskIn):
    data = task_in.model_dump()
    task = {**data, "id": 1}
    return task


@router.get("/tasks", response_model=Task, status_code=201)
async def tasks(task_in: TaskIn):
    data = task_in.model_dump()
    task = {**data, "id": 1}
    return task


@router.get("/download", response_model=Task, status_code=201)
async def download(task_in: TaskIn):
    data = task_in.model_dump()
    task = {**data, "id": 1}
    return task
