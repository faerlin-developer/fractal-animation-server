from app.common.db.user import BaseUserDatabaseClient
from app.task_master.db.queue import TaskQueueClient
from app.task_master.db.task import TaskDatabaseClient

REDIS_HOST = "redis-service"
REDIS_PORT = 6379
DATABASE_URL = "postgresql://myuser:mypassword@postgres-service:5432/mydb"

task_queue = TaskQueueClient(REDIS_HOST, REDIS_PORT)
user_db = BaseUserDatabaseClient(DATABASE_URL, force_rollback=False)
task_db = TaskDatabaseClient(DATABASE_URL, force_rollback=False)


def get_user_db() -> BaseUserDatabaseClient:
    return user_db


def get_task_db() -> TaskDatabaseClient:
    return task_db


def get_task_queue() -> TaskQueueClient:
    return task_queue


async def connect_database():
    await user_db.connect()
    await task_db.connect()


async def disconnect_database():
    await user_db.disconnect()
    await task_db.disconnect()
