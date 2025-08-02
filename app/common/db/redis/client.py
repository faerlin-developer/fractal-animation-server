import json
from dataclasses import asdict
from dataclasses import dataclass

import redis

QUEUE_NAME = "task_queue"


@dataclass
class FractalTask:
	id: int
	z_re: float
	z_im: float


class TaskQueue:

	def __init__(self, host: str, port: int):
		self.redis_client = redis.Redis(host=host, port=port)

	def push(self, task: FractalTask):
		""""""

		data = json.dumps(asdict(task))
		self.redis_client.rpush(QUEUE_NAME, data)

	def pop(self):
		return self.redis_client.blpop([QUEUE_NAME], timeout=5)
