from fastapi import APIRouter

from services.image_server.models.image import ImageIn, Image

router = APIRouter()


@router.post("/", response_model=Image, status_code=201)
async def create_post(image_in: ImageIn):
    data = image_in.model_dump()
    task = {**data, "id": 1}
    return task
