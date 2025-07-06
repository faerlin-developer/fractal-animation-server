from contextlib import asynccontextmanager

from fastapi import FastAPI

from services.image_server.routers.image import router as image_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Preparing resources")
    yield
    print("Tearing down resources")


app = FastAPI(lifespan=lifespan)

app.include_router(image_router)
