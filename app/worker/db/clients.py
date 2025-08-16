from common.db.minio.client import ObjectStorage
from common.db.redis.client import TaskQueue
from worker.config import cfg

task_queue = TaskQueue(cfg.redis_host, cfg.redis_port)
object_storage = ObjectStorage(cfg.minio_host, cfg.minio_port, cfg.minio_username, cfg.minio_password)
