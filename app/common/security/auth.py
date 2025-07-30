from fastapi import Request, status, HTTPException
from jwt import ExpiredSignatureError, PyJWTError, InvalidTokenError

from app.common.security.token import verify_jwt


async def authenticate(request: Request) -> dict:
    """Dependency to authenticate a user by verifying the request's JWT."""

    auth_header = request.headers.get("Authorization")
    scheme, _, token = auth_header.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid auth scheme")

    try:
        return verify_jwt(token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except (PyJWTError, InvalidTokenError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
