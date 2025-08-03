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

	@staticmethod
	def from_bytes(data: bytes):
		task_dict = json.loads(data)
		return FractalTask(**task_dict)


class TaskQueue:

	def __init__(self, host: str, port: int):
		self.redis_client = redis.Redis(host=host, port=port)

	def push(self, task: FractalTask):
		""""""

		data = json.dumps(asdict(task))
		self.redis_client.rpush(QUEUE_NAME, data)

	def pop(self, timeout=5):
		"""Pops the next element in the redis queue.
		   If the queue is empty, blocks for the specified timeout.
		   When blocking time exceeds timeout, return None.
		"""

		entry = self.redis_client.blpop([QUEUE_NAME], timeout=timeout)
		if entry is None:
			return None

		_, task_bytes = entry
		return FractalTask.from_bytes(task_bytes)
