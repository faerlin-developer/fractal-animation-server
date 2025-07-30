from fastapi import FastAPI

import app.common.logger.slog  # noqa: F401
from app.task_master.handlers.context import lifespan
from app.task_master.handlers.exception import general_exception_handler
from app.task_master.handlers.middleware import PreProcessRequest
from app.task_master.handlers.route import router

server = FastAPI(lifespan=lifespan)

# noinspection PyTypeChecker
server.add_middleware(PreProcessRequest)
server.add_exception_handler(Exception, general_exception_handler)
server.include_router(router)
