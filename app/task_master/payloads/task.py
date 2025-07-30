from pydantic import BaseModel


class AddTaskRequestPayload(BaseModel):
    z_re: float
    z_im: float


class AddTaskResponsePayload(AddTaskRequestPayload):
    id: int


class TaskIn(BaseModel):
    body: str


class Task(TaskIn):
    id: int
