import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.task_master.db.connections import database
from app.task_master.db.connections import r
from app.task_master.db.user import users
from app.task_master.routers.task import router as task_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Preparing resources")

    # Sample connection to asynchronous Redis
    await r.set('key', 'value 42')
    value = await r.get('key')
    logger.info(value)

    # Sample connection to postgres
    await database.connect()

    # Insert one user
    query = users.insert().values(username="Zoey", password_hash="<PASSWORD>")
    inserted_id = await database.execute(query)
    logger.info(f"Inserted user id: {inserted_id}")

    # Retrieve user by id
    query = users.select().where(users.c.id == inserted_id)
    user = await database.fetch_one(query)
    logger.info(f"Retrieved user: {user['username']}")

    yield

    await database.disconnect()

    logger.info("Tearing down resources")


app = FastAPI(lifespan=lifespan)
app.include_router(task_router)
