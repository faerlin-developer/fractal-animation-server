from fastapi import APIRouter

from services.task_master.models.tasks import Task, TaskIn

router = APIRouter()


@router.post("/tasks", response_model=Task, status_code=201)
async def create_post(task_in: TaskIn):
    data = task_in.model_dump()
    task = {**data, "id": 1}
    return task
