from contextlib import asynccontextmanager

from fastapi import FastAPI

from services.user_manager.routers.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Preparing resources")
    yield
    print("Tearing down resources")


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
