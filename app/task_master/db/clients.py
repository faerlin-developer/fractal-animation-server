from common.db.minio.client import ObjectStorage
from common.db.redis.client import TaskQueue
from common.db.sql.client import TaskDatabase, UserDatabase
from task_master.config import cfg

task_queue = TaskQueue(cfg.redis_host, cfg.redis_port)
user_db = UserDatabase(cfg.database_url, force_rollback=False)
task_db = TaskDatabase(cfg.database_url, force_rollback=False)
object_storage = ObjectStorage(cfg.minio_host, cfg.minio_port, cfg.minio_username, cfg.minio_password)


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
