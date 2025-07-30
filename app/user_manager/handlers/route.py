import time

import structlog
from fastapi import APIRouter, HTTPException
from fastapi import Request, Depends

from app.common.security.auth import authenticate
from app.common.security.crypt import hash_password
from app.common.security.token import create_jwt
from app.user_manager.db.clients import get_user_db
from app.user_manager.db.user import UserDatabaseClient
from app.user_manager.payloads.user import UserRequestPayload, SignUpResponsePayload, SignInResponsePayload

router = APIRouter()

log = structlog.get_logger()

from app.common.db.user import verify_user


@router.post("/sign-up", response_model=SignUpResponsePayload, status_code=201)
async def sign_up(request: Request, payload: UserRequestPayload, db: UserDatabaseClient = Depends(get_user_db)):
    """Creates a new user by storing credentials in database."""

    user = await db.get_user(payload.username)

    if user is not None:
        log.info(f"username already exists", username=user.username, request_id=request.state.request_id)
        raise HTTPException(status_code=409, detail="username already exists")

    new_id = await db.create_user(payload.username, hash_password(payload.password))
    log.info(f"created new user", id=new_id, username=payload.username, request_id=request.state.request_id)

    return {"id": new_id, "username": payload.username}


@router.delete("/delete-user", status_code=204)
async def delete_user(request: Request,
                      db: UserDatabaseClient = Depends(get_user_db),
                      claims: dict = Depends(authenticate)):
    """Delete a user from the database."""

    username = claims["sub"]
    log.info(f"deleting user", username=username, request_id=request.state.request_id)
    await db.delete_user(username)

    return None


@router.post("/sign-in", response_model=SignInResponsePayload, status_code=201)
async def sing_in(request: Request, payload: UserRequestPayload, db: UserDatabaseClient = Depends(get_user_db)):
    """Authenticate a user by responding with a JWT."""

    await verify_user(payload.username, db)
    expires_at = int(time.time()) + 3600
    token = create_jwt(payload.username, expires_at)

    return {"access_token": token, "token_type": "Bearer"}
