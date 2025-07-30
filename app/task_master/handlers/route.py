import structlog
from fastapi import APIRouter, Depends, Request

from app.common.db.task import FractalTask
from app.common.db.user import BaseUserDatabaseClient
from app.common.db.user import verify_user
from app.common.security.auth import authenticate
from app.common.tables.task import State
from app.task_master.db.clients import get_task_queue, get_user_db, get_task_db
from app.task_master.db.queue import TaskQueueClient
from app.task_master.db.task import TaskDatabaseClient
from app.task_master.payloads.task import AddTaskRequestPayload, AddTaskResponsePayload
from app.task_master.payloads.task import Task, TaskIn

router = APIRouter()

log = structlog.get_logger()


@router.post("/add", response_model=AddTaskResponsePayload, status_code=201)
async def add(request: Request,
			  payload: AddTaskRequestPayload,
			  user_db: BaseUserDatabaseClient = Depends(get_user_db),
			  task_db: TaskDatabaseClient = Depends(get_task_db),
			  queue: TaskQueueClient = Depends(get_task_queue),
			  claims: dict = Depends(authenticate)):
	""""""

	username = claims["sub"]
	await verify_user(username, user_db)

	task_id = await task_db.add(username, payload.z_re, payload.z_im, State.READY)
	task = FractalTask(id=task_id, z_re=payload.z_re, z_im=payload.z_im)
	await queue.push(task)

	log.info("added task", task_id=task_id, request_id=request.state.request_id)

	return {"id": task_id, "z_re": payload.z_re, "z_im": payload.z_im}


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
async def download(task_in: TaskIn, claims: dict = Depends(authenticate)):
	data = task_in.model_dump()
	task = {**data, "id": 1}
	return task
