from pydantic import BaseModel


class TaskIn(BaseModel):
    body: str


class Task(TaskIn):
    id: int
