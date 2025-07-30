import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class PreProcessRequest(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        """Pre-process request object."""

        unique_id = uuid.uuid4()
        request_id = request.headers.get("X-Request-ID", str(unique_id))
        request.state.request_id = request_id

        return await call_next(request)
