from contextlib import asynccontextmanager

from fastapi import FastAPI

from services.task_master.routers.task import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Preparing resources")
    yield
    print("Tearing down resources")


app = FastAPI(lifespan=lifespan)

app.include_router(task_router)
