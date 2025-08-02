from pydantic import BaseModel


class TaskIn(BaseModel):
	z_re: float
	z_im: float


class Task(TaskIn):
	id: int
	state: str
	url: str
