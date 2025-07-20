from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.user_manager.db.instances import connect_database, disconnect_database


@asynccontextmanager
async def lifespan(application: FastAPI):
    print("Initialize resources")
    await connect_database()
    yield
    print("Tear down resources")
    await disconnect_database()
