from common.db.minio.client import ObjectStorage
from common.db.redis.client import TaskQueue
from common.db.sql.client import TaskDatabase, UserDatabase

REDIS_HOST = "redis-service"
REDIS_PORT = 6379
DATABASE_URL = "postgresql://myuser:mypassword@postgres-service:5432/mydb"
MINIO_URL = "172.17.0.1:9000"
MINIO_USERNAME = "minioadmin"
MINIO_PASSWORD = "minioadmin"

task_queue = TaskQueue(REDIS_HOST, REDIS_PORT)
user_db = UserDatabase(DATABASE_URL, force_rollback=False)
task_db = TaskDatabase(DATABASE_URL, force_rollback=False)
object_storage = ObjectStorage(MINIO_URL, MINIO_USERNAME, MINIO_PASSWORD)


def get_user_db() -> UserDatabase:
	return user_db


def get_task_db() -> TaskDatabase:
	return task_db


def get_task_queue() -> TaskQueue:
	return task_queue


def get_object_storage() -> ObjectStorage:
	return object_storage


async def connect_database():
	await user_db.connect()
	await task_db.connect()


async def disconnect_database():
	await user_db.disconnect()
	await task_db.disconnect()
