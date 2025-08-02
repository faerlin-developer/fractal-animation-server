import structlog
from fastapi import APIRouter, Depends, Request, HTTPException

from common.db.redis.client import FractalTask
from common.db.redis.client import TaskQueue
from common.db.sql.client import UserDatabase, TaskDatabase
from common.db.sql.tables.task import State
from common.security.auth import authenticate
from task_master.db.clients import get_task_queue, get_user_db, get_task_db, get_object_storage
from task_master.payloads.task import TaskIn, Task

router = APIRouter()

log = structlog.get_logger()


@router.post("/add", response_model=Task, status_code=201)
async def add(request: Request,
			  payload: TaskIn,
			  user_db: UserDatabase = Depends(get_user_db),
			  task_db: TaskDatabase = Depends(get_task_db),
			  task_queue: TaskQueue = Depends(get_task_queue),
			  claims: dict = Depends(authenticate)):
	""""""

	username = claims["sub"]
	verified = await user_db.verify_user(username)
	if not verified:
		raise HTTPException(status_code=409, detail="username does not exists")

	task_id = await task_db.add(username, payload.z_re, payload.z_im, State.READY)
	task = FractalTask(id=task_id, z_re=payload.z_re, z_im=payload.z_im)
	task_queue.push(task)

	log.info("added task", task_id=task_id, request_id=request.state.request_id)

	return Task(id=task_id, z_re=payload.z_re, z_im=payload.z_im, state=State.READY, url="")


@router.post("/delete", status_code=201)
async def delete():
	return None


@router.get("/tasks", status_code=201)
async def tasks():
	return None


@router.get("/download/{task_id}", response_model=Task, status_code=201)
async def download(task_id: int,
				   user_db: UserDatabase = Depends(get_user_db),
				   task_db: TaskDatabase = Depends(get_task_db),
				   claims: dict = Depends(authenticate),
				   object_storage=Depends(get_object_storage)):
	""""""

	username = claims["sub"]
	verified = await user_db.verify_user(username)
	if not verified:
		raise HTTPException(status_code=409, detail="username does not exists")

	task = await task_db.get_task(task_id)
	if task is None:
		raise HTTPException(status_code=409, detail="task does not exists")

	url = object_storage.get(bucket_name="images", object_name=f"{task_id}.png")
	return Task(id=task.id, z_re=task.z_re, z_im=task.z_im, state=task.state, url=url)
