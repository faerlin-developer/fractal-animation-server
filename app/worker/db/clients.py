from common.db.minio.client import ObjectStorage
from common.db.redis.client import TaskQueue

REDIS_HOST = "redis-service"
REDIS_PORT = 6379
DATABASE_URL = "postgresql://myuser:mypassword@postgres-service:5432/mydb"
MINIO_URL = "172.17.0.1:9000"
MINIO_USERNAME = "minioadmin"
MINIO_PASSWORD = "minioadmin"

task_queue = TaskQueue(REDIS_HOST, REDIS_PORT)
object_storage = ObjectStorage(MINIO_URL, MINIO_USERNAME, MINIO_PASSWORD)
