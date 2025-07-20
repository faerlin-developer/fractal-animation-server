import time

import structlog
from fastapi import APIRouter, HTTPException
from fastapi import Request, Depends, status
from jwt import ExpiredSignatureError, PyJWTError, InvalidTokenError

from app.common.security.crypt import hash_password
from app.common.security.token import create_jwt, verify_jwt
from app.user_manager.db.instances import get_user_database
from app.user_manager.db.user import UserDatabase
from app.user_manager.payloads.user import UserRequestPayload, SignUpResponsePayload, SignInResponsePayload

router = APIRouter()

log = structlog.get_logger()


@router.post("/sign-up", response_model=SignUpResponsePayload, status_code=201)
async def sign_up(request: Request, payload: UserRequestPayload, db: UserDatabase = Depends(get_user_database)):
    """Creates a new user by storing credentials in database."""

    user = await db.get_user(payload.username)

    if user is not None:
        log.info(f"username already exists", username=user.username, request_id=request.state.request_id)
        raise HTTPException(status_code=409, detail="username already exists")

    new_id = await db.create_user(payload.username, hash_password(payload.password))
    log.info(f"created new user", id=new_id, username=payload.username, request_id=request.state.request_id)

    return {"id": new_id, "username": payload.username}


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


@router.delete("/delete-user", status_code=204, dependencies=[Depends(authenticate)])
async def delete_user(request: Request,
                      db: UserDatabase = Depends(get_user_database),
                      claims: dict = Depends(authenticate)):
    """Delete a user from the database."""

    username = claims["sub"]
    log.info(f"deleting user", username=username, request_id=request.state.request_id)
    await db.delete_user(username)

    return None


@router.post("/sign-in", response_model=SignInResponsePayload, status_code=201)
async def sing_in(request: Request, payload: UserRequestPayload, db: UserDatabase = Depends(get_user_database)):
    """Authenticate a user by responding with a JWT."""

    user = await db.get_user(payload.username)

    if user is None:
        log.info(f"username does not exists", username=payload.username, request_id=request.state.request_id)
        raise HTTPException(status_code=409, detail="username does not exists")

    expires_at = int(time.time()) + 3600
    token = create_jwt(user.username, expires_at)

    return {"access_token": token, "token_type": "Bearer"}
