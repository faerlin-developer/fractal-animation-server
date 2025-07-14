import databases
import redis.asyncio as redis

DATABASE_URL = "postgresql://myuser:mypassword@postgres-service:5432/mydb"

r = redis.Redis(host='redis-service', port=6379)

database = databases.Database(
    DATABASE_URL,
    force_rollback=False
)
