from fastapi import APIRouter

from services.user_manager.models.user import UserIn, User

router = APIRouter()


@router.post("/sign-up", response_model=User, status_code=201)
async def sign_up(user_in: UserIn):
    data = user_in.model_dump()
    task = {**data, "id": 1}
    return task


@router.get("/sign-in", response_model=User, status_code=201)
async def sing_in(user_in: UserIn):
    data = user_in.model_dump()
    task = {**data, "id": 1}
    return task
