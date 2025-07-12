from fastapi import APIRouter

from services.task_master.models.tasks import Task, TaskIn

router = APIRouter()


@router.post("/add", response_model=Task, status_code=201)
async def add(task_in: TaskIn):
    data = task_in.model_dump()
    task = {**data, "id": 1}
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
