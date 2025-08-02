import time

import structlog
from fastapi import APIRouter, HTTPException
from fastapi import Request, Depends

from common.db.sql.client import UserDatabase
from common.security.auth import authenticate
from common.security.crypt import hash_password
from common.security.token import create_jwt
from user_manager.db.clients import get_user_db
from user_manager.payloads.user import UserRequest, SignUp, SignIn

router = APIRouter()

log = structlog.get_logger()


@router.post("/sign-up", response_model=SignUp, status_code=201)
async def sign_up(request: Request, payload: UserRequest, db: UserDatabase = Depends(get_user_db)):
	"""Creates a new user by storing credentials in database."""

	user = await db.get_user(payload.username)

	if user is not None:
		log.info(f"username already exists", username=user.username, request_id=request.state.request_id)
		raise HTTPException(status_code=409, detail="username already exists")

	new_id = await db.create_user(payload.username, hash_password(payload.password))
	log.info(f"created new user", id=new_id, username=payload.username, request_id=request.state.request_id)

	return SignUp(id=new_id, username=payload.username, password="")


@router.delete("/delete-user", status_code=204)
async def delete_user(request: Request,
					  db: UserDatabase = Depends(get_user_db),
					  claims: dict = Depends(authenticate)):
	"""Delete a user from the database."""

	username = claims["sub"]
	log.info(f"deleting user", username=username, request_id=request.state.request_id)
	await db.delete_user(username)

	return None


@router.post("/sign-in", response_model=SignIn, status_code=201)
async def sing_in(request: Request, payload: UserRequest, db: UserDatabase = Depends(get_user_db)):
	"""Authenticate a user by responding with a JWT."""

	verified = await db.verify_user(payload.username)
	if not verified:
		raise HTTPException(status_code=409, detail="username does not exists")

	expires_at = int(time.time()) + 3600
	token = create_jwt(payload.username, expires_at)

	return SignIn(access_token=token, token_type="Bearer")
