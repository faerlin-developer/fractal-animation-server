from fastapi import APIRouter

from services.image_server.models.image import ImageIn, Image

router = APIRouter()


@router.get("/download", response_model=Image, status_code=201)
async def download(image_in: ImageIn):
    data = image_in.model_dump()
    task = {**data, "id": 1}
    return task
