import json
from dataclasses import asdict

import redis.asyncio as redis

from app.common.db.task import FractalTask

QUEUE_NAME = "task_queue"


class TaskQueueClient:

    def __init__(self, host: str, port: int):
        self.redis_client = redis.Redis(host=host, port=port)

    async def push(self, task: FractalTask):
        """"""

        data = json.dumps(asdict(task))
        await self.redis_client.rpush(QUEUE_NAME, data)

    async def pop(self):
        pass
