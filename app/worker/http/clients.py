import httpx

from common.db.sql.tables.task import State
from worker.config import cfg


class TaskMasterClient:

	def __init__(self, host: str, port: int):
		self.client = httpx.Client()
		self.host = host
		self.port = port

	def update_state(self, task_id: int, state: State):
		payload = {"state": state}
		self.client.put(f"http://{self.host}:{self.port}/update_state/{task_id}", json=payload)


task_master_client = TaskMasterClient(cfg.task_master_host, cfg.task_master_port)
